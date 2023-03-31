from typing import Container, Optional, Type

from pydantic import BaseConfig, BaseModel, create_model


class OrmConfig(BaseConfig):
    orm_mode = True
