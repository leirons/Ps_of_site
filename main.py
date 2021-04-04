import requests
import bs4
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('wb')


class Client:
    def __init__(self):
        self.session = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"
        }
        self.dict1 = []

    def load_page(self, pages: int = None):
        url = 'https://uvex-safety.ru/products/eyewear'
        self.host = 'https://uvex-safety.ru/'
        res = self.session.get(url=url)
        res.raise_for_status()
        return res.text

    def parser(self, text: str):
        src = bs4.BeautifulSoup(text, 'lxml')
        products = src.select('div.product')
        for urls in products:
            self.get_url(url=urls)

    def get_url(self, url):
        get_url = self.host + url.find('a').get('href')  # Ссылка на товар
        if not get_url:
            logger.error("Url is not found")
        else:
            self.parser_in_url(url=get_url)

    def parser_in_url(self, url):
        res1 = requests.get(url=url).text
        soup1 = bs4.BeautifulSoup(res1, 'lxml')

        title = soup1.find('h1').text
        if not title:
            logger.error("Title is not found")

        Articul = soup1.find('p').text
        if not Articul:
            logger.error("Articul is not found")

        records = []
        content = soup1.find('div', class_='media-body').find_all('li')
        if not content:
            logger.error("Content is not found")
        else:
            for text in content:
                records.append(text.text.strip())

        self.dict1.append({
            'Title': title,
            'Content': records,
            'Articul': Articul,

        })

    def save_to_file(self):
        with open('Собранные данные12.json', 'a', encoding='utf-8') as file:
            json.dump(self.dict1, file, indent=4, ensure_ascii=False)

    def run(self):
        text = self.load_page()
        self.parser(text=text)
        self.save_to_file()


if __name__ == '__main__':
    parser = Client()
    parser.run()