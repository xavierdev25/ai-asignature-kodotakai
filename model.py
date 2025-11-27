import requests
import json

OLLAMA_URL = "http://localhost:11434/api/embeddings"
MODEL = "mxbai-embed-large"

with open("simpsons_episodes.json", "r", encoding="utf-8") as f:
    episodes = json.load(f)

embeddings_data = []

for ep in episodes:
    text = f"{ep['name']} - {ep['synopsis']}"
    print(f"Procesando: {ep['name']}")

    response = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": text})
    embedding = response.json()["embedding"]

    embeddings_data.append({
        "id": ep["id"],
        "name": ep["name"],
        "season": ep["season"],
        "synopsis": ep["synopsis"],
        "embedding": embedding
    })

with open("simpsons_embeddings_ollama.json", "w", encoding="utf-8") as f:
    json.dump(embeddings_data, f, ensure_ascii=False, indent=2)

print("Embeddings creados con Ollama y guardados en simpsons_embeddings_ollama.json")
