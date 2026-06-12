from fastapi import FastAPI

app = FastAPI(
    title="QCCP School Simulator",
    version="1.0.0"
)

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "qccp-school-simulator"
    }
