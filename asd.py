import os
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))  # Default to 5000 if PORT is not set
    uvicorn.run(app, host="0.0.0.0", port=port)
