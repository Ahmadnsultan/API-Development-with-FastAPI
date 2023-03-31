from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException, APIRouter
from .. import models, schemas,utils
from ..database import get_db
router = APIRouter(
    prefix="/user",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user_validate: schemas.UserCreate, db: Session = Depends(get_db)):
    user = models.User(**user_validate.dict())
    email_exist = db.query(models.User).filter(models.User.email == user.email).first()
    if email_exist:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Email already registered")
    user.password = utils.hash(user.password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the user with id: {id} not found")

    return user
