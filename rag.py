import json
import numpy as np
import faiss
import requests

EMBED_MODEL = "mxbai-embed-large"
LLM_MODEL = "qwen2.5:3b-instruct"
OLLAMA_URL = "http://localhost:11434"

with open("simpsons_embeddings_ollama.json", "r", encoding="utf-8") as f:
    episodes = json.load(f)

vectors = np.array([ep["embedding"] for ep in episodes]).astype("float32")

index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)

def embed_text(text: str):
    """Genera el embedding del texto usando Ollama"""
    response = requests.post(f"{OLLAMA_URL}/api/embeddings", json={
        "model": EMBED_MODEL,
        "prompt": text
    })
    return np.array(response.json()["embedding"]).astype("float32")

def search_similar_episodes(query, top_k=5):
    """Busca los episodios más similares al texto dado"""
    query_emb = embed_text(query).reshape(1, -1)
    distances, indices = index.search(query_emb, top_k)
    return [episodes[i] for i in indices[0]]

def generate_response(query, context_episodes):
    """Genera una respuesta usando un modelo LLM (Mistral, Qwen, Llama, etc.)"""
    context_text = "\n".join(
        [ep["name_en"] if "name_en" in ep else ep["name"] for ep in context_episodes]
    )

    prompt = (
        "Eres un experto en la serie *Los Simpson*. "
        "Basándote únicamente en la siguiente lista de títulos de episodios, responde solo con el título exacto (en inglés) del episodio más relevante para la pregunta del usuario. No añadas ningún texto adicional, solo el título exacto.\n\n"
        f"Pregunta del usuario:\n{query}\n\n"
        f"Episodios relevantes:\n{context_text}\n\n"
        "Respuesta:"
    )
    response = requests.post(f"{OLLAMA_URL}/api/generate", json={
        "model": LLM_MODEL,
        "prompt": prompt
    }, stream=True)

    full_text = ""
    try:
        for line in response.iter_lines():
            if not line:
                continue
            try:
                data = json.loads(line.decode("utf-8"))
            except Exception as e:
                print("[ERROR] No se pudo decodificar una línea JSON:", e)
                print("[DEBUG] Línea:", line)
                continue
            if "response" in data:
                full_text += data["response"]
            elif "error" in data:
                print("[ERROR] Ollama:", data["error"])
                return f"[ERROR] Ollama: {data['error']}"
        return full_text.strip()
    except Exception as e:
        print("[ERROR] Error procesando la respuesta de Ollama:", e)
        return "[ERROR] Error procesando la respuesta de Ollama."

if __name__ == "__main__":
    user_query = input("💬 Pregunta: ")

    print("\n🔎 Buscando episodios similares...")
    similar = search_similar_episodes(user_query, top_k=5)

    print("\n📺 Episodios relevantes:")
    for ep in similar:
        print(f" - {ep['name']} (T{ep['season']})")

    print("\n🤖 Generando respuesta...\n")
    answer = generate_response(user_query, similar)
    print(answer)
