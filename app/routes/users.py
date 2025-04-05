from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..db import get_db
from ..auth.auth import hash_password, authenticate_user, create_access_token, get_user_by_email
from ..websocket_manager import websocket_manager

router = APIRouter()

@router.post("/register", response_model=schemas.UserOut)
async def register_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new user.
    
    Args:
        user: User registration details
        db: Database session
        
    Returns:
        Newly created user
    """
    existing_user = await get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    hashed_password = hash_password(user.password)
    new_user = models.User(email=user.email, password=hashed_password)

    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)

    #Notify websocket
    await websocket_manager.broadcast_new_user(f"Welcome {new_user.email}!")
    return schemas.UserOut.from_orm(new_user) 



@router.post("/login", response_model=schemas.Token)
async def login_user(user: schemas.UserLogin, db: AsyncSession = Depends(get_db)):
    """
    Authenticate user and generate access token.
    
    Args:
        user: Login credentials
        db: Database session
        
    Returns:
        JWT access token
    """
    db_user = await authenticate_user(db, email=user.email, password=user.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

