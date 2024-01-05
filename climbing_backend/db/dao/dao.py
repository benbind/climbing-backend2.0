from typing import Any, Optional, Sequence, Type, Union

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from climbing_backend.db.base import Base
from climbing_backend.db.dependencies import get_db_session
from climbing_backend.db.models.models import Climb, Climber, Comment, Location, Post


class GenericDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_model(
        self,
        model_class: Type[Base],
        object_dto: BaseModel,
    ) -> None:
        new_object = model_class(**object_dto.model_dump())
        self.session.add(new_object)
        await self.session.commit()
        await self.session.refresh(new_object)

    async def get_model_by_id(
        self,
        model_class: Type[Base],
        item_id: int,
    ) -> Optional[Base]:
        return await self.session.get(model_class, item_id)

    async def delete_model(self, model_class: Type[Base], item_id: int) -> None:
        item = await self.session.get(model_class, item_id)
        if item is not None:
            await self.session.delete(item)
            await self.session.commit()

    async def update(
        self,
        model_class: Type[Base],
        item_id: int,
        update_data: dict[Any, Any],
    ) -> None:
        item = await self.session.get(model_class, item_id)
        if item:
            for key, value in update_data.items():
                setattr(item, key, value)
            await self.session.commit()
            await self.session.refresh(item)

    async def get_posts_by_climber(self, climber_id: int) -> Sequence[Any]:
        result = await self.session.execute(
            select(Post).where(Post.climber_id == climber_id),
        )
        return result.scalars().all()

    async def get_posts_by_climb(self, climb_id: int) -> Sequence[Any]:
        result = await self.session.execute(
            select(Post).where(Post.climb_id == climb_id),
        )
        return result.scalars().all()

    async def get_climbs_by_location(self, location_id: int) -> Sequence[Any]:
        result = await self.session.execute(
            select(Climb).where(Climb.location_id == location_id),
        )
        return result.scalars().all()

    async def get_model_by_name(
        self,
        model_class: Type[Union[Climber, Climb, Location]],
        name: str,
    ) -> Sequence[Any]:
        search_term = f"%{name}%"
        result = await self.session.execute(
            select(model_class).where(
                func.lower(model_class.name).like(func.lower(search_term)),
            ),
        )
        return result.scalars().all()

    async def get_comments_by_post(self, post_id: int) -> Sequence[Any]:
        result = await self.session.execute(
            select(Comment).where(Comment.post_id == post_id),
        )
        return result.scalars().all()
