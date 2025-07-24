from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from .models import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, name: str, email: str) -> User:
        """사용자 생성"""
        user = User(name=name, email=email)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def get_all(self) -> List[User]:
        """모든 사용자 조회"""
        result = await self.session.execute(select(User))
        return result.scalars().all()