from fastapi import FastAPI
from parser import fetch_tenders
import uvicorn

app = FastAPI(title="Tender API")

@app.get("/tenders")
def get_tenders(limit: int = 100):
    return fetch_tenders(limit).to_dict(orient="records")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)