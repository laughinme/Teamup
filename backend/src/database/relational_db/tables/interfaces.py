from typing import TypeVar, Generic

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

from .table_base import Base

T = TypeVar("T", bound=Base)
PKType = TypeVar("PKType")


class BaseInterface(Generic[T, PKType]):
    """
    Generic async repository like helper with common crud helpers.

    Concrete interfaces should inherit from this class and pass the sqlalchemy
    model they operate on. This keeps method implementations like `add` and
    `get_by_id` in one place.
    """

    def __init__(self, model: type[T], session: AsyncSession):
        if not isinstance(model, DeclarativeMeta):
            raise TypeError("model must inherit from SQLAlchemy declarative base")

        self.model = model
        self.session = session

    @property
    def pk_column(self):
        """
        Return the single primary key column for the model.
        """
        mapper = self.model.__mapper__
        primary_key = mapper.primary_key

        if len(primary_key) != 1:
            raise ValueError(
                f"{self.model.__name__} must have exactly one primary key column to use BaseInterface"
            )

        return primary_key[0]

    async def add(self, instance: T) -> T:
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def get_by_id(self, id: PKType) -> T | None:
        stmt = select(self.model).where(self.pk_column == id)
        return await self.session.scalar(stmt)
    
    async def delete(self, id: PKType) -> int:
        """Delete by primary key, returns number of rows deleted."""
        stmt = delete(self.model).where(self.pk_column == id)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount or 0
    
    
    # TODO: Add more generic methods when needed
    # async def list(self, *, limit: int | None = None, offset: int | None = None) -> Sequence[T]:
    #     stmt = select(self.model)

    #     if limit is not None:
    #         stmt = stmt.limit(limit)
    #     if offset is not None:
    #         stmt = stmt.offset(offset)

    #     result = await self.session.scalars(stmt)
    #     return result.all()
    
    # async def add_many(self, instances: Iterable[T]) -> Sequence[T]:
    #     instances = tuple(instances)
    #     if not instances:
    #         return ()

    #     self.session.add_all(instances)
    #     await self.session.flush()
    #     return instances

    # async def update_fields(self, id: PKType, values: Mapping[str, Any]) -> T | None:
    #     """
    #     Partial update helper. Returns the updated model if it exists.
    #     """
    #     if not values:
    #         return await self.get_by_id(id)

    #     stmt = (
    #         update(self.model)
    #         .where(self.pk_column == id)
    #         .values(**values)
    #         .returning(self.model)
    #     )

    #     result = await self.session.execute(stmt)
    #     await self.session.flush()
    #     row = result.scalar_one_or_none()

    #     return row
