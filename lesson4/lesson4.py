import requests
from datetime import datetime
from lxml import html
from pymongo import MongoClient
from pprint import pprint

mail_news = 'https://news.mail.ru'
lenta_news = 'https://lenta.ru/'
yandex_news = 'https://yandex.ru/news/'


def scraper(url1, url2, url3):
    all_news = []
    now_date = datetime.today().strftime('%d-%m-%Y')

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
    main_url = url1
    response = requests.get(main_url, headers=header)
    dom = html.fromstring(response.text)

    mail_news_dom = dom.xpath('//li[@class="list__item"]/a')

    for el in mail_news_dom:
        mail_news_dict = {}

        source = 'news.mail.ru'
        title = el.xpath('.//text()')
        link = el.xpath('.//@href')
        date = now_date

        mail_news_dict['source'] = source
        mail_news_dict['title'] = title
        mail_news_dict['link'] = link
        mail_news_dict['date'] = date

        all_news.append(mail_news_dict)


    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
    main_url = url2
    response = requests.get(main_url, headers=header)
    dom = html.fromstring(response.text)

    lenta_news_dom = dom.xpath('//section[@class="b-yellow-box js-yellow-box"]//div//a')

    for el in lenta_news_dom:
        lenta_news_dict = {}

        source = 'lenta.ru'
        title = el.xpath('.//text()')
        link = el.xpath('.//@href')
        date = now_date

        lenta_news_dict['source'] = source
        lenta_news_dict['title'] = title
        lenta_news_dict['link'] = link
        lenta_news_dict['date'] = date

        all_news.append(lenta_news_dict)

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
    main_url = url3
    response = requests.get(main_url, headers=header)
    dom = html.fromstring(response.text)

    yandex_news_dom = dom.xpath('//article')

    for el in yandex_news_dom:
        yandex_news_dict = {}

        source = el.xpath('.//span//a//@aria-label')
        title = el.xpath('.//h2[@class="mg-card__title"]//text()')
        link = el.xpath('.//div[@class="mg-card__inner"]/a/@href | .//div[@class="mg-card__text"]/a/@href')
        date = now_date + ' ' + el.xpath('.//span[@class="mg-card-source__time"]//text()')[0]

        yandex_news_dict['source'] = source
        yandex_news_dict['title'] = title
        yandex_news_dict['link'] = link
        yandex_news_dict['date'] = date

        all_news.append(yandex_news_dict)
    return all_news


def save_db(data_news):
    client = MongoClient('localhost', 27017)
    db = client['news']
    news = db.news
    news.insert_many(data_news)
    return news


day_news = scraper(mail_news, lenta_news, yandex_news)
save_db(day_news)
pprint(day_news)
