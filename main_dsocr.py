from transformers import AutoModel, AutoTokenizer
import torch
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "2"
model_name = "/data01/kilm/users/quocvh/HF/models/deepseek-ai/DeepSeek-OCR"

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModel.from_pretrained(
    model_name,
    _attn_implementation="flash_attention_2",
    trust_remote_code=True,
    use_safetensors=True,
)
model = model.eval().cuda().to(torch.bfloat16)

import fitz
import os
from tqdm.auto import tqdm
from PIL import Image
from io import BytesIO


def parse_pdf(path):
    doc = fitz.open(path)

    md_pages = []
    for i in tqdm(range(len(doc))):
        page = doc.load_page(i)
        pix = page.get_pixmap()
        img = Image.open(BytesIO(pix.tobytes("png")))

        image_file = "./tmp/page.jpg"
        output_path = "./tmp"
        img.save(image_file)

        # prompt = "<image>\nFree OCR. "
        prompt = "<image>\n<|grounding|>Convert the document to markdown. "
        # image_file = 'vng.jpg'
        # output_path = './vng'

        # infer(self, tokenizer, prompt='', image_file='', output_path = ' ', base_size = 1024, image_size = 640, crop_mode = True, test_compress = False, save_results = False):

        # Tiny: base_size = 512, image_size = 512, crop_mode = False
        # Small: base_size = 640, image_size = 640, crop_mode = False
        # Base: base_size = 1024, image_size = 1024, crop_mode = False
        # Large: base_size = 1280, image_size = 1280, crop_mode = False

        # Gundam: base_size = 1024, image_size = 640, crop_mode = True

        res = model.infer(
            tokenizer,
            prompt=prompt,
            image_file=image_file,
            output_path=output_path,
            base_size=1024,
            image_size=640,
            crop_mode=True,
            save_results=True,
            test_compress=True,
        )

        with open(output_path + "/result.mmd") as f:
            md = f.read()

            md_pages.append(md)

    name = path.split("/")[-1].replace(".pdf", "")

    output = f"submit4/dsocr_training/{name}/main.md"

    os.makedirs(output.rsplit("/", 1)[0], exist_ok=True)

    with open(output, "w") as f:
        f.write("\n\n".join(md_pages))


import re
import os
import glob


def norm_data(data):
    # data = re.sub(r"<table>.*?</table>", "", data)

    # data = data.replace("<table>", "<table><thead></thead><tbody>").replace("</table>", "</tbody></table>")

    data = re.sub(
        r"<table>.*?(Lần ban hành|VIETTEL AI RACE).*?</table>",
        "",
        data,
        count=0,
        flags=0,
    )
    data = re.sub(r"VIETTEL AI RACE.*?Lần ban hành: 1", "", data, flags=re.DOTALL)

    imgs = re.findall(r"!\[\]\(images/.*?.jpg\)", data)

    i = 0
    for m in imgs:
        idx = data.find(m)
        # print(data[idx: idx+50])

        if "[Hình" in data[idx : idx + 50]:
            data = data.replace(m, f"|<image_{i+1}>|", 1)
            i += 1
        else:
            data = data.replace(m, "", 1)

    data = re.sub(r"</table>[ \n]*<table>", "", data, flags=re.DOTALL)

    data = re.sub(r"\n#+?(\d+)\. ", r"\n#\1\. ", data, flags=re.DOTALL)

    data = re.sub(r"\n#+ ([^\d])", r"\n\1", data, flags=re.DOTALL)

    data = re.sub(r"\n#* ?(\d+\.) ", r"\n# ", data, flags=re.DOTALL)
    data = re.sub(r"\n#* ?(\d+\.\d+) ", r"\n## ", data, flags=re.DOTALL)
    data = re.sub(r"\n#* ?(\d+\.\d+\.\d+) ", r"\n### ", data, flags=re.DOTALL)
    # data = re.sub(r"\n#* ?Hình (\d+)", r"\nHình \1", data, flags=re.DOTALL)

    return data


import re
import os
import glob


paths = sorted(glob.glob("submit4/dsocr_public/*/main.md"))
for path in paths:
    with open(path) as f:
        data = f.read()

    # name = path.split("/")[-2]
    # data = f"# {name}\n\n" + data

    # print(data)
    new_path = path.replace("dsocr_public/", "dsocr_public_v10/")
    print(new_path)

    os.makedirs(new_path.rsplit("/", 1)[0], exist_ok=True)

    data = norm_data(data)

    with open(new_path, "w") as f:
        f.write(data)

    # break


import pandas as pd

SET = "public"
QA_PATH = f"submit4/qa_{SET}_v3.csv"
df = pd.read_csv(QA_PATH)
subdf = df[["num_correct", "answers"]]


import os
import glob

INPUT_DIR = "data4/public_test_input"
OUTPUT_DIR = "submit4/dsocr_public_v10"

answer_md = os.path.join(OUTPUT_DIR, "answer.md")

with open(answer_md, "w", encoding="utf-8") as f:
    f.write("### TASK EXTRACT\n")
    for pdf_path in sorted(glob.glob(os.path.join(INPUT_DIR, "*.pdf"))):
        pdf_name = pdf_path.split("/")[-1].replace(".pdf", "")
        with open(
            os.path.join(OUTPUT_DIR, pdf_name, "main.md"),
            "r",
            encoding="utf-8",
        ) as md:
            f.write(md.read())
            f.write("\n")

    f.write("\n\n")
    f.write("### TASK QA\n")
    f.write(subdf.to_csv(index=False))

import shutil

shutil.copy("var_pdf/main_v1.py", OUTPUT_DIR)
shutil.make_archive(OUTPUT_DIR, "zip", OUTPUT_DIR)
