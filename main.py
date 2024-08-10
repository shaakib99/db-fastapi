from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
import os

def lifespan(app):
    load_dotenv()
    yield

app = FastAPI(lifespan=lifespan)

# routes
@app.get("/")
def hello():
    return "hello"


# Start application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port = int(os.getenv("PORT", "8000")), reload=True)