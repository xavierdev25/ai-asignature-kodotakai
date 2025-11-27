import requests
import json

all_episodes = []

for page in range(1, 40):
    url = f"https://thesimpsonsapi.com/api/episodes?page={page}"
    response = requests.get(url)
    data = response.json()
    all_episodes.extend(data["results"])

with open("simpsons_episodes.json", "w", encoding="utf-8") as f:
    json.dump(all_episodes, f, ensure_ascii=False, indent=2)

print(f"Descargados {len(all_episodes)} episodios")
