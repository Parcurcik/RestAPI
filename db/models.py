from sqlalchemy import Column, Integer, String, DateTime
from db.database import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    topic = Column(String)
    datetime = Column(String)
