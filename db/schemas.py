from pydantic import BaseModel


class NewsBase(BaseModel):
    title: str
    topic: str


class NewsCreate(NewsBase):
    pass


class News(NewsBase):
    id: int
    datetime: str

    class Config:
        orm_mode = True
