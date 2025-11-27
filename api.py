
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from rag import search_similar_episodes, generate_response

app = FastAPI(title="Simpsons RAG API")

class AskRequest(BaseModel):
	question: str
	top_k: int = 5

class Episode(BaseModel):
	id: int
	name: str
	season: int
	synopsis: str

class AskResponse(BaseModel):
	answer: str
	episodes: List[Episode]


@app.post("/ask", response_model=AskResponse)
async def ask_simpsons(req: AskRequest):
	try:
		similar = search_similar_episodes(req.question, top_k=req.top_k)
		answer = generate_response(req.question, similar)
		episodes_out = [
			Episode(
				id=ep["id"],
				name=ep["name"],
				season=ep["season"],
				synopsis=ep["synopsis"]
			) for ep in similar
		]
		return AskResponse(answer=answer, episodes=episodes_out)
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
