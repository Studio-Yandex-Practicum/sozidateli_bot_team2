from typing import List, TypeVar

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import ObjectIsNoneException


ModelType = TypeVar("ModelType")


class BaseRepository:
    """Базовый репозиторий для моделей."""

    def __init__(self, model: ModelType, session_factory: AsyncSession):
        self.model = model
        self.session = session_factory

    async def get_list(self) -> List[ModelType]:
        """Получить полный список объектов."""
        async with self.session as session:
            db_objs = await session.execute(select(self.model))
            return db_objs.scalars().all()

    async def create(self, obj_in) -> ModelType:
        """Создать объект."""
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        async with self.session as session:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def get_by_attributes(self, **kwargs) -> ModelType:
        """Получить объект по указанным атрибутам."""
        try:
            async with self.session as session:
                conditions = [
                    getattr(self.model, attribute_name) == search_value
                    for attribute_name, search_value in kwargs.items()
                ]
                obj = await session.execute(
                    select(self.model).where(or_(*conditions))
                )
                obj = obj.scalars().first()
            if obj is None:
                raise ObjectIsNoneException()
            return obj
        except AttributeError:
            raise ObjectIsNoneException()

    async def remove(self, db_obj) -> ModelType:
        """Удалить объект."""
        async with self.session as session:
            await session.delete(db_obj)
            await session.commit()
        return db_obj
