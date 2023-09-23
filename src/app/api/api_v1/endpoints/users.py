from typing import Any, List
from fastapi import Body, Depends, APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from app import schemas
from sqlalchemy.orm import Session
from app.database import SessionLocal
from sqlalchemy.orm import Session

from app import schemas, models
from app.api import deps
import app.crud.user as user_crud


router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User)
def create_user(
    user_body: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    db_user = user_crud.get_user_by_email(db, email=user_body.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db, user=user_body)


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_body = schemas.UserUpdate(**current_user_data)
    if password:
        user_body.password = password
    if full_name:
        user_body.full_name = full_name
    if email:
        user_body.email = email
    user = user_crud.update_user(db, current_user, user_body)
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.get("/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int,
    user_body: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(get_db),
) -> Any:
    db_user = user_crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    db_user = user_crud.update_user(db, db_user, user_body)
    return db_user
