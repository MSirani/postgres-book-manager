from pydantic import BaseModel, ConfigDict, Field


class AuthorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    bio: str | None = None


class AuthorUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    bio: str | None = None


class AuthorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    bio: str | None


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=500)
    author_id: int


class BookUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=500)
    author_id: int


class BookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    author_id: int


class BookWithAuthor(BaseModel):
    id: int
    title: str
    description: str | None
    author: AuthorOut
