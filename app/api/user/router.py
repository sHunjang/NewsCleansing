from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from .service import UserService
from .schemas import UserCreate, UserResponse

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """사용자 생성"""
    try:
        service = UserService(db)
        return await service.create_user(user_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"사용자 생성 실패: {str(e)}"
        )

@router.get("/", response_model=List[UserResponse])
async def get_users(
    db: AsyncSession = Depends(get_db)
):
    """모든 사용자 조회"""
    service = UserService(db)
    return await service.get_users()