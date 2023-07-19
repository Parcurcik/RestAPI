import time
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

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


def check_title(session, title):
    return session.query(News).filter_by(title=title).first() is not None


def get_product_url():
    yesterday = datetime.now() - timedelta(days=1)
    date_str = yesterday.strftime('%Y/%m/%d')
    product_url = f'https://news.rambler.ru/{date_str}/'
    return product_url


def parse_news():
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    product_url = get_product_url()

    local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = local_session()

    driver.get(product_url)

    scroll_pause_time = 0.5

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
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
        title = title_element.get_text() if title_element else None
        topic = topic.get_text() if topic else None
        time_str = time_element.get_text() if time_element else None

        if title is None or topic is None or time_str is None:
            continue
        if 'назад' in time_str:
            date = datetime.now().strftime('%Y-%m-%d')
        else:
            day, month = time_str.split()
            month_number = month_dict[month]
            current_year = datetime.now().year
            time_obj = datetime(current_year, month_number, int(day))
            date = time_obj.strftime('%Y-%m-%d')

        if not check_title(session, title):
            news = News(title=title, topic=topic, datetime=date)
            session.add(news)

    session.commit()
