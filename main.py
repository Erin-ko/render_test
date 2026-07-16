from fastapi import FastAPI

app = FastAPI(
    title="Hello API",
    description="A simple FastAPI application to be deployed on Render",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Hello"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
