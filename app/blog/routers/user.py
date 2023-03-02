from fastapi import APIRouter
from blog import schemas, database, oauth2
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, status
from blog.repository import user


router = APIRouter(
    prefix="/user",
    dependencies=[Depends(oauth2.get_current_user)],
    tags=["users"]
)

get_db = database.get_db


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create_user(request, db)
    

@router.get("/", response_model=List[schemas.ShowUser])
def get_all(db: Session = Depends(get_db)):
    return user.get_all(db)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.get_user(id, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    return user.delete_user(id, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_user(id: int, request: schemas.User, db: Session = Depends(get_db)):
    return user.update_user(id, request, db)
