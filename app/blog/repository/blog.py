from sqlalchemy.orm import Session
from blog import models, schemas
from fastapi import status, HTTPException


def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def create_blog(request: schemas.Blog, db: Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def get_blog(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} is not found" )
    return blog


def delete_blog(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} is not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return "Blog is deleted"


def update_blog(id: int, request: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} is not found")
    blog.update({"title": request.title, "body": request.body})
    db.commit()
    return "Updated"
