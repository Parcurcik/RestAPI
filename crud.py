from sqlalchemy.orm import Session
from db import models, schemas
import datetime

current_date = datetime.date.today()
date = str(current_date.strftime("%Y-%m-%d"))


def get_news_by_id(db: Session, news_id: int):
    return db.query(models.News).filter(models.News.id == news_id).first()


def get_news_by_title(db: Session, title: str):
    return db.query(models.News).filter(models.News.title == title).first()


def get_news_by_key(db: Session, key: str):
    return db.query(models.News).filter(models.News.title.contains(key)).all()


def get_news_by_topic(db: Session, topic: str):
    return db.query(models.News).filter(models.News.topic == topic).all()


def get_news(db: Session, skip: int = 0, limit: int = 2000):
    return db.query(models.News).offset(skip).limit(limit).all()


def create_news(db: Session, item: schemas.NewsCreate):
    db_news = models.News(
        title=item.title,
        topic=item.topic,
        datetime=date
    )
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news


def update_news(db: Session, item: schemas.NewsCreate, news_id: int):
    db_item = get_news_by_id(db, news_id=news_id)
    db_item.title = item.title
    db_item.topic = item.topic
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_news(db: Session, news_id: int):
    db_item = get_news_by_id(db, news_id=news_id)
    db.delete(db_item)
    db.commit()
