from fastapi import FastAPI
from book import router as book_router

app = FastAPI()

app.include_router(book_router)


@app.get("/")
def read_root():
    return {
        "statusCode": 200,
        "error": None,
        "message": "API đang chạy",
        "data": None
    }
