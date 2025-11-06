from typing import Dict, Type
from sqlmodel import SQLModel

_models: Dict[str, Type[SQLModel]] = {}

def register_model(model: Type[SQLModel]) -> Type[SQLModel]:
    """Register a model in the global registry"""
    _models[model.__name__] = model
    return model