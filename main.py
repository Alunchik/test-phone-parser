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
    # Регулярное выражение для поиска всех номеров с кодом +7/8 и без него, в разных форматах. Выделяем в группы значимые цифры номера (без +7/8)

    # не захватывает номера без кода города
    # reg_exp = r'[7|8]?[\s-]?\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})'

    # захватывает номера без кода города
    reg_exp = r'[7|8]?[\s-]?\(?(\d{3})?\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})[^\d]'
    groups = re.findall(reg_exp, text)
    return groups


# Принимает кортежи с группами цифр в номерах (3-4 группы цифр)
def format_phones(unformated_nums):
    nums = []
    for num in unformated_nums:
        # если нет кода города, добавляем московский
        if num[0] == '':
            groups = ('8', '495', num[1], num[2], num[3])
        else:
            groups = ('8', num[0], num[1], num[2], num[3])
        number = ''.join(groups)
        nums.append(number)
    return nums


if __name__ == '__main__':
    URL = "https://targetsms.ru/blog/1074-format-telefonnykh-nomerov"
    print(format_phones(get_phones(get_page(URL))))
