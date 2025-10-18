import os
import pandas as pd
import shutil
import pymupdf4llm
import glob


SET = "public"
# SET = "private"

INPUT_DIR = f"../data2/{SET}_test_input"
QA_PATH = f"../submit2/qa_{SET}.csv"
if os.path.exists(QA_PATH):
    OUTPUT_DIR = f"../submit2/pymuf4llm_search_{SET}_output"
else:
    OUTPUT_DIR = f"../submit2/pymuf4llm_{SET}_output"

def extract_to_markdown(pdf_path, md_path):
    pdf_name = pdf_path.split("/")[-1].replace(".pdf", "").replace("Public", "Public_")

    md_text = pymupdf4llm.to_markdown(pdf_path)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# {pdf_name}\n\n")
        f.write(md_text)


def baseline_extraction(input_dir, output_dir):
    for pdf_path in glob.glob(os.path.join(input_dir, "*.pdf")):
        pdf_name = pdf_path.split("/")[-1]
        out_folder = os.path.join(output_dir, pdf_name.replace(".pdf", ""))
        os.makedirs(out_folder, exist_ok=True)
        md_path = os.path.join(out_folder, "main.md")
        extract_to_markdown(pdf_path, md_path)
        print(f"Đã trích xuất {pdf_path} -> {md_path}")


def baseline_qa(question_csv_path):
    df = pd.read_csv(question_csv_path)
    items = []
    for idx, row in df.iterrows():
        items.append({"num_correct": 1, "answers": "A"})
    subdf = pd.DataFrame(items)

    return subdf


if __name__ == "__main__":
    baseline_extraction(INPUT_DIR, OUTPUT_DIR)
    question_csv = os.path.join(INPUT_DIR, "question.csv")
    answer_md = os.path.join(OUTPUT_DIR, "answer.md")
    
    if os.path.exists(QA_PATH):
        df = pd.read_csv(QA_PATH)
        subdf = df[["num_correct", "answers"]]
    else:
        subdf = baseline_qa(question_csv)


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
        f.write("### TASK QA\n")
        f.write(subdf.to_csv(index=False))

    shutil.copy("main_v1.py", OUTPUT_DIR)
    shutil.make_archive(OUTPUT_DIR, "zip", OUTPUT_DIR)
