from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Book
from schemas import BookBase, BaseResponse

router = APIRouter()


@router.get("/books", response_model=BaseResponse)
def get_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return BaseResponse(statusCode=200, message="Lấy danh sách sách thành công", data=books)


@router.get("/books/search", response_model=BaseResponse)
def search_books(category: str, db: Session = Depends(get_db)):
    books = db.query(Book).filter(Book.category.like(f"%{category}%")).all()
    return BaseResponse(statusCode=200, message="Tìm kiếm thành công", data=books)


@router.get("/books/{book_id}", response_model=BaseResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        return BaseResponse(statusCode=404, error="Not Found", message="Không tìm thấy sách", data=None)
    return BaseResponse(statusCode=200, message="Lấy chi tiết sách thành công", data=book)


@router.post("/books", response_model=BaseResponse)
def create_book(book: BookBase, db: Session = Depends(get_db)):
    new_book = Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return BaseResponse(statusCode=201, message="Thêm sách thành công", data=new_book)


@router.put("/books/{book_id}", response_model=BaseResponse)
def update_book(book_id: int, book: BookBase, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        return BaseResponse(statusCode=404, error="Not Found", message="Không tìm thấy sách", data=None)

    for key, value in book.dict().items():
        setattr(db_book, key, value)

    db.commit()
    return BaseResponse(statusCode=200, message="Cập nhật sách thành công", data=None)


@router.delete("/books/{book_id}", response_model=BaseResponse)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        return BaseResponse(statusCode=404, error="Not Found", message="Không tìm thấy sách", data=None)

    db.delete(db_book)
    db.commit()
    return BaseResponse(statusCode=200, message="Xóa sách thành công", data=None)
