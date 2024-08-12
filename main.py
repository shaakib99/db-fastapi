from database.service import DatabaseService
from demo.router import router as DemoRouter
from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
import os

def lifespan(app):
    load_dotenv()

    # check database connection
    db_service = DatabaseService(None)
    db_service.connect()
    db_service.create_metadata()
    yield

app = FastAPI(lifespan=lifespan)

# routes
routes = [DemoRouter]
for route in routes:
    app.include_router(route)


# Start application
if __name__ == "__main__":
    print(os.getenv("PORT"))
    uvicorn.run("main:app", host="0.0.0.0", port = int(os.getenv("PORT", "8000")), reload=True)