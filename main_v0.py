import os
import pdfplumber
import pandas as pd
import shutil

INPUT_DIR = "../data/public_test_input"
OUTPUT_DIR = "../submit/baseline_output"


def extract_to_markdown(pdf_path, md_path):
    with pdfplumber.open(pdf_path) as pdf, open(md_path, "w", encoding="utf-8") as f:
        for i, page in enumerate(pdf.pages):

            text = page.extract_text()
            if text:
                f.write(text.strip() + "\n\n")

            tables = page.extract_tables()
            for ti, table in enumerate(tables):
                f.write(f"### Table {ti+1}\n")
                f.write("<table>\n")
                for row in table:
                    f.write(
                        "<tr>"
                        + "".join(f"<td>{cell if cell else ''}</td>" for cell in row)
                        + "</tr>\n"
                    )
                f.write("</table>\n\n")

            image_dir = os.path.join(os.path.dirname(md_path), "images")
            os.makedirs(image_dir, exist_ok=True)

            j = 0
            for _, img in enumerate(page.images):
                x0, top, x1, bottom = img["x0"], img["top"], img["x1"], img["bottom"]
                if x1 - x0 < 100 or bottom - top < 100:
                    continue

                j += 1
                cropped = page.within_bbox((x0, top, x1, bottom)).to_image(
                    resolution=300
                )
                img_path = os.path.join(image_dir, f"image{j}.jpg")
                cropped.original.save(img_path, "JPEG")
                f.write(f"![](images/image{j}.jpg)\n\n")


def baseline_extraction(input_dir, output_dir):
    for fname in os.listdir(input_dir):
        if fname.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, fname)
            out_folder = os.path.join(output_dir, fname.replace(".pdf", ""))
            os.makedirs(out_folder, exist_ok=True)
            md_path = os.path.join(out_folder, "main.md")
            extract_to_markdown(pdf_path, md_path)
            print(f"Đã trích xuất {fname} -> {md_path}")


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
    subdf = baseline_qa(question_csv)

    with open(answer_md, "w", encoding="utf-8") as f:
        f.write("### TASK EXTRACT\n")
        for fname in os.listdir(INPUT_DIR):
            if fname.endswith(".pdf"):
                f.write(f"# {fname}\n\n")
                with open(
                    os.path.join(OUTPUT_DIR, fname.replace(".pdf", ""), "main.md"),
                    "r",
                    encoding="utf-8",
                ) as md:
                    f.write(md.read())

        f.write("\n")
        f.write("### TASK QA\n")
        f.write(subdf.to_csv(index=False))

    shutil.copy("main.py", OUTPUT_DIR)
    shutil.make_archive(OUTPUT_DIR, "zip", OUTPUT_DIR)
