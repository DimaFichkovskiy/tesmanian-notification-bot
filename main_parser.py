import time
import lxml
import asyncio
from http import HTTPStatus

import requests
from bs4 import BeautifulSoup

from models import DBDriver
from bot import send_notification
from config import EMAIL, PASSWORD

MAIN_URL = "https://www.tesmanian.com/blogs/tesmanian-blog"
LOGIN_URL = "https://www.tesmanian.com/account/login"
USER_AGENT = {
    "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}


def start_parser():
    requests_session = login()
    while True:
        request = get_request(session=requests_session, url=MAIN_URL)

        soup = BeautifulSoup(request.text, 'lxml')
        articles_data = soup.find_all("div", {"class": "eleven columns omega align_left"})

        exist_news = [i.url for i in DBDriver.get_last_news()]

        for article in articles_data:
            data = article.find("a")
            title = data.get_text()
            url = "https://www.tesmanian.com/" + data.get("href")

            if url not in exist_news:
                DBDriver.add_new_news(title=title, url=url)
                parsed_data = {
                    "title": title,
                    "url": url
                }

                a = asyncio.gather(send_notification(**parsed_data))
                asyncio.get_event_loop().run_until_complete(a)

        time.sleep(15)


def login():
    login_data = {'customer[email]': EMAIL, 'customer[password]': PASSWORD}
    with requests.Session() as requests_session:
        post = requests_session.post(LOGIN_URL, data=login_data, headers=USER_AGENT)
        if post.status_code != HTTPStatus.OK:
            return login()
        return requests_session


def get_request(session: requests.Session, url: str):
    try:
        with session:
            request = session.get(url)
            if request.status_code == HTTPStatus.UNAUTHORIZED:
                requests_session = login()
                request = get_request(session=requests_session, url=url)
                return request
            return request
    except requests.exceptions.ConnectionError:
        return get_request(session=session, url=url)


if __name__ == '__main__':
    start_parser()
