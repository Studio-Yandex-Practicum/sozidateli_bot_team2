from abc import ABC, abstractmethod
from typing import Any, Sequence, TypeVar

from sqlalchemy import delete, insert, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db import Base


ModelType = TypeVar("ModelType", bound=Base)


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self):
        ...

    @abstractmethod
    async def update_one(self):
        ...

    @abstractmethod
    async def find_one(self):
        ...

    @abstractmethod
    async def find_all(self):
        ...

    @abstractmethod
    async def delete_one(self):
        ...


class SQLAlchemyRepository(AbstractRepository):
    model: ModelType | None = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_one(self, **kwargs: dict[str, Any]) -> ModelType:
        stmt = insert(self.model).values(**kwargs).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def update_one(self, id: int, **kwargs: dict[str, Any]) -> ModelType:
        kwargs = {
            key: value for key, value in kwargs.items() if value is not None
        }
        stmt = (
            update(self.model)
            .values(**kwargs)
            .filter_by(id=id)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def find_one(self, **filter_by: dict[str, Any]) -> ModelType | None:
        filters = [
            getattr(self.model, key) == value
            for key, value in filter_by.items()
        ]
        stmt = select(self.model).filter(or_(*filters))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_all(self) -> Sequence[ModelType]:
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete_one(self, **filter_by: dict[str, Any]) -> ModelType:
        stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def find_all_by_attrs(
        self, **filter_by: dict[str, Any]
    ) -> ModelType | None:
        filters = [
            getattr(self.model, key) == value
            for key, value in filter_by.items()
        ]
        stmt = select(self.model).filter(or_(*filters))
        result = await self.session.execute(stmt)
        return result.scalars().all()
