from fastapi import APIRouter
from blog import schemas, database, oauth2
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, status
from blog.repository import blog


router = APIRouter(
    prefix="/blog",
    dependencies=[Depends(oauth2.get_current_user)],
    tags=["blogs"]
)

get_db = database.get_db


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.create_blog(request, db)


@router.get("/", response_model=List[schemas.ShowBlog])
def get_all(db: Session = Depends(get_db)):
    return blog.get_all(db)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_blog(id: int, db: Session = Depends(get_db)):
    return blog.get_blog(id, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db)):
    return blog.delete_blog(id, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.update_blog(id, request, db)
