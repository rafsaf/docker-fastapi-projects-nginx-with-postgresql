from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from tortoise.models import Model
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get_one(self, id: Any) -> Optional[ModelType]:
        query = await self.model.get(id=id)
        return query

    async def get_multi(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        query = await self.model.all().offset(skip).limit(100)
        return list(query)

    async def create_one(self, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = await self.model.create(**obj_in_data)
        return db_obj

    async def update_one(
        self, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        await db_obj.save()
        return db_obj

    async def remove_one(self, id: int) -> None:
        await self.model.filter(id=id).delete()
