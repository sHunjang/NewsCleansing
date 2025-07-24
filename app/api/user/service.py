from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .repository import UserRepository
from .schemas import UserCreate, UserResponse

class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)
    
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """사용자 생성"""
        user = await self.repository.create(
            name=user_data.name,
            email=user_data.email
        )
        return UserResponse.model_validate(user)
    
    async def get_users(self) -> List[UserResponse]:
        """모든 사용자 조회"""
        users = await self.repository.get_all()
        return [UserResponse.model_validate(user) for user in users]
