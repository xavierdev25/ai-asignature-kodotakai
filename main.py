from sentence_transformers import SentenceTransformer
import json
import numpy as np

model = SentenceTransformer('sentence-transformers/distiluse-base-multilingual-cased-v2')

with open("simpsons_episodes.json", "r", encoding="utf-8") as f:
    episodes = json.load(f)

embeddings_data = []

for ep in episodes:
    text = f"{ep['name']} - {ep['synopsis']}"
    embedding = model.encode(text).tolist()

    embeddings_data.append({
        "id": ep["id"],
        "name": ep["name"],
        "season": ep["season"],
        "synopsis": ep["synopsis"],
        "embedding": embedding
    })

with open("simpsons_embeddings.json", "w", encoding="utf-8") as f:
    json.dump(embeddings_data, f, ensure_ascii=False, indent=2)

print("Embeddings creados correctamente ✅")
