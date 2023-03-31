from typing import Container, Optional, Type, Any

from pony.orm.core import Collection, Entity
from pydantic import BaseModel, create_model


class OrmModel(BaseModel):
    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls: Type[BaseModel], obj: Any) -> BaseModel:
        def normalize(value):
            if isinstance(value, Entity):
                return value.get_pk()
            if hasattr(value, '_entity_'):
                return list(value)
            return value

        new_obj = type('_NewObj_', (object, ), {})
        for attr in obj._adict_.keys():
            setattr(new_obj, attr, normalize(getattr(obj, attr)))

        return super().from_orm(new_obj)


def pony_to_pydantic(
    db_model: Type,
    *,
    base: Type = OrmModel,
    exclude: Container[str] = []
) -> Type[BaseModel]:
    fields = {}
    for name, attr in db_model._adict_.items():
        if not isinstance(attr, Collection):
            if name in exclude:
                continue

            python_type: Optional[type] = attr.py_type
            if attr.is_relation:
                python_type = attr.py_type._pk_.py_type

            default = None
            if attr.default is None and not attr.nullable:
                default = ...
            fields[name] = (python_type, default)

    pydantic_model = create_model(
        db_model.__name__,
        __base__=base,
        **fields  # type: ignore
    )
    return pydantic_model
