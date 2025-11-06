from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import openai

client = MongoClient("mongodb://localhost:27017/")
db = client["scraper_db"]
collection = db["cleaned_data"]

docs = list(collection.find({}, {"url": 1, "clean_text": 1, "_id": 0}))
texts = [d["clean_text"] for d in docs]
urls = [d["url"] for d in docs]

print("Generating embeddings for documents...")
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(texts, show_progress_bar=True)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings, dtype=np.float32))
print(f"Indexed {len(texts)} documents in FAISS.")

def semantic_search(query, top_k=3):
    query_vec = model.encode([query])
    D, I = index.search(np.array(query_vec, dtype=np.float32), top_k)
    results = []
    for i, idx in enumerate(I[0]):
        results.append({
            "url": urls[idx],
            "text": texts[idx][:400] + "...",
            "score": float(D[0][i])
        })
    return results

query = input("Enter a question: ")
results = semantic_search(query)
print("\nTop related documents:")
for r in results:
    print(f"\n🔗 {r['url']}\nScore: {r['score']:.4f}\nExcerpt: {r['text']}")
