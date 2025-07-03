from pydantic import BaseModel


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
