from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import threading
import time

import crud
from db import schemas, models
from db.database import SessionLocal, engine
from parser import parse_news

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def run_parser():
    while True:
        parse_news()
        time.sleep(1200)


parser_thread = threading.Thread(target=run_parser)
parser_thread.start()


@app.get("/news/", response_model=list[schemas.News])
def get_all_news(skip: int = 0, limit: int = 2000, db: Session = Depends(get_db)):
    news = crud.get_news(db, skip=skip, limit=limit)
    if not news:
        raise HTTPException(status_code=404, detail="Please, add some articles")
    return news


@app.get("/news/find/{news_id}", response_model=schemas.News)
def find_news_by_id(news_id: int, db: Session = Depends(get_db)):
    db_news = crud.get_news_by_id(db, news_id=news_id)
    if not db_news:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_news


@app.get("/news/find_by_topic/{topic}", response_model=list[schemas.News])
def find_news_by_topic(topic: str, db: Session = Depends(get_db)):
    db_news = crud.get_news_by_topic(db, topic=topic.title())
    if not db_news:
        raise HTTPException(status_code=404, detail="This topic is not found")
    return db_news


@app.get("/news/find_by_key/{key}", response_model=list[schemas.News])
def find_news_by_key(key: str, db: Session = Depends(get_db)):
    db_news = crud.get_news_by_key(db, key=key)
    if not db_news:
        raise HTTPException(status_code=404, detail="This key is not found in all articles")
    return db_news


@app.post("/news/create", response_model=schemas.News)
def create_news(item: schemas.NewsCreate, db: Session = Depends(get_db)):
    db_news = crud.get_news_by_title(db, title=item.title)
    if db_news and db_news.title == item.title:
        raise HTTPException(status_code=400, detail='Article with this title already exists')
    return crud.create_news(db=db, item=item)


@app.put("/news/update/{news_id}", response_model=schemas.News)
def update_news(news_id: int, item: schemas.NewsCreate, db: Session = Depends(get_db)):
    db_news = crud.get_news_by_id(db, news_id=news_id)
    if not db_news:
        raise HTTPException(status_code=400, detail='Article not found')
    return crud.update_news(db=db, item=item, news_id=news_id)


@app.delete("/news/delete/{news_id}", response_model=dict)
def delete_news(news_id: int, db: Session = Depends(get_db)):
    db_news = crud.get_news_by_id(db, news_id=news_id)
    if not db_news:
        raise HTTPException(status_code=400, detail='Article not found')
    crud.delete_news(db=db, news_id=news_id)
    return {'status': "ok"}
