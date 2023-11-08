#
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs


# Получаем необходимый текст со страницы
def get_page(url):
    options = Options()
    options.add_argument('headless')

    browser = webdriver.Chrome(options=options)
    browser.get(url)

    # Ищем номер телефона только в теле сайта, метаданные и прочее нам не нужны

    body = browser.find_element(By.TAG_NAME, 'body')
    return body.text

# Получаем из текста номера телефонов
def get_phones(text):
    reg_exp = r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
    return re.findall(reg_exp, text)

if __name__ == '__main__':
    URL = "https://repetitors.info/"
    print(get_phones(get_page(URL)))
