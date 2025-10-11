import os

os.environ["CUDA_VISIBLE_DEVICES"] = "2"

import pandas as pd

from vllm import LLM, SamplingParams


# df = pd.read_csv("../data/public_test_input/question.csv")
df = pd.read_csv("qa_private_search.csv")

data = df.to_dict("records")


# TEMPLATE = """Hãy chọn các đáp án đúng cho câu hỏi trắc nghiệm sau
# Ouput format: Các đáp án đúng cách nhau bởi dấu ",", eg: A,B,C,D
# Chỉ trả về các chữ cái ABCD, không trả kèm gì thêm

# Câu hỏi: {Question}
# A. {A}
# B. {B}
# C. {C}
# D. {D}
# """

TEMPLATE = """Hãy chọn các đáp án đúng cho câu hỏi trắc nghiệm sau dựa vào tài liệu
Ouput format: Các đáp án đúng cách nhau bởi dấu ",", eg: A,B,C,D
Chỉ trả về các chữ cái ABCD, không trả kèm gì thêm

Tài liệu: {context}

Câu hỏi: {Question}
A. {A}
B. {B}
C. {C}
D. {D}
"""


x = data[0]
print(TEMPLATE.format(**x))


llm = LLM(model="/mnt/nfs-data/kilm-storage/public-llm/Qwen2.5-3B-Instruct")

MM = []
for x in data:
    prompt = TEMPLATE.format(**x)
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]
    MM.append(messages)


sampling_params = SamplingParams(temperature=0.0, top_k=1, max_tokens=256)
outputs = llm.chat(MM, sampling_params)


preds = []
for x in outputs:
    res = x.outputs[0].text
    answers = []
    for a in res.split(","):
        a = a.split(".")[0].strip()

        if a:
            a = a[0]
        else:
            continue

        if a in "ABCD":
            answers.append(a)

    if not answers:
        preds.append("A")
    else:
        preds.append(",".join(answers))

df["num_correct"] = [len(x.split(",")) for x in preds]
df["answers"] = preds

df.to_csv("qa_public_pred.csv", encoding="utf-8-sig", index=False)
