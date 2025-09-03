from typing import Any

from pydantic import BaseModel, Field


class Read(BaseModel):
    web_id: str
    name: str
    description: str
    version: str

    @classmethod
    def from_model(cls, obj):
        return cls(
            web_id=obj.meta.web_id,
            name=obj.meta.name,
            description=obj.meta.description,
            version=obj.meta.version,
        )


class InvokePlugin(BaseModel):
    text: str | None = None
    language: str = Field(default="russian")
    data: dict[str, Any] | None = None
