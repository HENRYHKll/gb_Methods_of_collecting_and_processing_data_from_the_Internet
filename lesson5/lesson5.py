from itertools import count

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ES
from selenium.webdriver.common.by import By
from pprint import pprint
from pymongo import MongoClient
import time
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['email']
email = db.email

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver: WebDriver = webdriver.Chrome()

driver.get("https://mail.ru")

login = driver.find_element(By.NAME, 'login')
login.send_keys('log@mail.ru')
login.send_keys(Keys.ENTER)

password = driver.find_element(By.NAME, 'password')
time.sleep(1)
password.send_keys('passs')
password.send_keys(Keys.ENTER)
time.sleep(2)
items = driver.find_elements(By.CLASS_NAME, 'llc')
time.sleep(1)


def extraction_link_email():
    time.sleep(0.5)
    links_page = set()
    for item in items:
        links_page.add(item.get_attribute('href'))
    return links_page


def scroll():
    actions = ActionChains(driver)
    articles = driver.find_elements(By.CLASS_NAME, 'llc')
    actions.move_to_element(articles[-1]).perform()


def collection_link_emal():
    links_emails = set()

    for i in range(2):
        links_emails.update(extraction_link_email())
        scroll()

    return links_emails


def check_bd(data):
    do = True
    for _ in email.find({'link': data['link']}):
        do = False
        return data.clear()

    email.insert_one(data)
    return data


def scrap_mail_content():
    all_links_emails = collection_link_emal()
    data = []
    count = 0
    for link in all_links_emails:
        driver.get(link)
        time.sleep(1)
        data_temp = {
            'link': link,
            'title': driver.find_element(By.CLASS_NAME, 'thread__subject').text,
            'mail_from': driver.find_element(By.CLASS_NAME, 'letter-contact').text,
            'data': driver.find_element(By.CLASS_NAME, 'letter__date').text,
            "message": driver.find_element(By.CLASS_NAME, 'letter-body').text
        }
        requestBD = check_bd(data_temp)
        if bool(requestBD):
            data.append(data_temp)
            count += 1

    return data


mails = scrap_mail_content()
pprint('new mail ', '/n', mails)

driver.quit()