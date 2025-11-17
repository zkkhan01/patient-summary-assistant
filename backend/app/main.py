from fastapi import FastAPI
from .routers import patients, summaries

app = FastAPI(
    title="Patient Summary Assistant API",
    description="Track 1 - Patient Summary Assistant using Pathway as the live index",
    version="0.2.0",
)

app.include_router(patients.router)
app.include_router(summaries.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
