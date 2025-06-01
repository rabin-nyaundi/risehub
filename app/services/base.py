from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session
from app.db.repositories.base import BaseRepository

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    def get_by_id(self, id: int) -> Optional[ModelType]:
        return self.repository.get_by_id(id)

    def get_all(self) -> List[ModelType]:
        return self.repository.get_all()

    def create(self, schema: CreateSchemaType) -> ModelType:
        return self.repository.create(**schema.dict())

    def update(self, id: int, schema: UpdateSchemaType) -> Optional[ModelType]:
        return self.repository.update(id, **schema.dict(exclude_unset=True))

    def delete(self, id: int) -> bool:
        return self.repository.delete(id)

    def verify_ownership(self, id: int, user_id: int) -> bool:
        instance = self.get_by_id(id)
        return instance and instance.user_id == user_id 