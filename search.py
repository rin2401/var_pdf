import os

os.environ["CUDA_VISIBLE_DEVICES"] = "2"

import glob
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-m3")


paths = glob.glob("../submit/pymuf4llm_public_output/*/*.md")


docs = []

for path in paths:
    with open(path) as f:
        text = f.read()

    # print(len(text.split()))
    docs.append(text)


docs_embedding = model.encode(docs)


df = pd.read_csv("../data/public_test_input/question.csv")


contexts = []
for query in df["Question"]:
    query_embedding = model.encode([query])
    similarities = cosine_similarity(query_embedding, docs_embedding)
    idx = np.argmax(similarities)
    print(paths[idx], similarities[0][idx])
    contexts.append(docs[idx])

df["context"] = contexts

df.to_csv("qa_public_search.csv", encoding="utf-8-sig", index=False)
