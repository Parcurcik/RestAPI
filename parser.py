import time
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from db.database import engine
from db.models import News

month_dict = {
    'января': 1,
    'февраля': 2,
    'марта': 3,
    'апреля': 4,
    'мая': 5,
    'июня': 6,
    'июля': 7,
    'августа': 8,
    'сентября': 9,
    'октября': 10,
    'ноября': 11,
    'декабря': 12
}

PRODUCT_URL = 'https://news.rambler.ru/2023/07/01/'

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

driver = webdriver.Chrome()
driver.get(PRODUCT_URL)

SCROLL_PAUSE_TIME = 0.5

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

html = driver.page_source
driver.close()
driver.quit()

soup = bs(html, 'lxml')
cards = soup.find_all('div', class_='_1rqVu')

for card in cards:
    title_element = card.find('a', class_='rui__2H432zN')
    topic = card.find('span', class_='rui__36rfxc7')
    time_element = card.find('span', class_='rui__1CeQYIJ')
    title = title_element.get_text()
    topic = topic.get_text()
    time_str = time_element.get_text()

    day, month = time_str.split()
    month_number = month_dict[month]
    current_year = datetime.now().year
    time_obj = datetime(current_year, month_number, int(day))
    date = time_obj.strftime('%Y-%m-%d')

    news = News(title=title, topic=topic, datetime=date)
    session.add(news)


session.commit()
