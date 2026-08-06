from pydantic import BaseModel, Field, ConfigDict

class CuisineBase(BaseModel):
    name: str = Field(max_length=100)
    country_code: str | None = Field(None, min_length=1, max_length=3)

class CuisineCreate(CuisineBase):
    pass

class CuisineRead(CuisineBase):
    id: int
    slug: str | None = Field(max_length=110)

    model_config = ConfigDict(from_attributes=True)