from fastapi import FastAPI

app = FastAPI(title="Heroes API")

@app.get("/")
async def root():
    return {"status": "running"}
