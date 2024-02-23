from pydantic import BaseModel, Field


class GroupSerializer(BaseModel):
    title: str
    description: str


class MediaSerializer(BaseModel):
    type: str
