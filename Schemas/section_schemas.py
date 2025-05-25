from pydantic import BaseModel

class SectionBase(BaseModel):
    name: str
    description: str

class SectionCreate(SectionBase):
    pass

class SectionUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class Section(SectionBase):
    id: int

    class Config:
        from_attributes = True