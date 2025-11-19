from typing import Generic, TypeVar, Any
from pydantic import BaseModel, Field, TypeAdapter

T = TypeVar('T')

# class CursorInfo(BaseModel):
#     next_cursor: str | None = Field(None, description='Opaque cursor for the next page')
#     sort: str | None = Field(None, description='Sort preset slug')
#     keys: list[Any] = Field(..., description='List of keys to filter by in the order of current sorting preset')
#     filters_hash: str = Field(..., description='Hash of the filters used to fetch the current page')
    
#     has_next_page: bool = Field(...)

class CursorPage(BaseModel, Generic[T]):
    items: list[T] = Field(...)
    next_cursor: str | None = Field(
        None,
        # description='Opaque cursor for the next page. Its left here for backwards compatibility.',
        # deprecated=True,
    )
    # cursor: str | None = Field(None, description='Opaque cursor for the next page')
    

    # @classmethod
    # def from_list(cls, items: list[Any], next_cursor: str | None):
    #     adapter = TypeAdapter(cls)
    #     return adapter.validate_python(
    #         {'items': items, 'next_cursor': next_cursor},
    #         from_attributes=True,
    #     )
