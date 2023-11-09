import re
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs


# Получаем необходимый текст со страницы
# Selenium управляет браузером и позволяет скрапить динамически-создаваемый контент тоже
def get_page(url):
    options = Options()
    options.add_argument('headless')
    browser = webdriver.Chrome(options=options)
    browser.get(url)
    for elem in browser.find_elements(By.CSS_SELECTOR, ".phone-number_hidden"):
        try:
            elem.click()
        except Exception:
            pass

    # for elem in browser.find_elements(By.CSS_SELECTOR, "button"):
    #     if elem.is_displayed():
    #         try:
    #             elem.click()
    #         except Exception:
    #             pass

    # body = body_elem.GetAttribute("innerHTML")
    # soup = bs(body, 'html.parser')

    # для поиска номера телефона нам нужно тело запроса
    body_elem = browser.find_element(By.TAG_NAME, 'body')
    return body_elem.text


# Получаем из текста номера телефонов
def get_phones(text):
    text = ''.join(('\n', text, '\n'))

    # не захватывает номера без кода города
    # reg_exp = r'[7|8]?[\s-]?\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})'

    # Регулярное выражение для поиска всех номеров с кодом +7/8 и без него, в разных форматах. Выделяем в группы значимые цифры номера (без +7/8)
    # захватывает номера без кода города
    reg_exp = r'\D[7|8]?[\s-]?\(?(\d{3})?\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})\D'
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


# URL адрес передается как аргумент командной строки

if __name__ == '__main__':
    URL = sys.argv[1]
    # Получаем контент со страницы в т.ч. и динамически сгенерированный
    # Далее ищем номера регулярным выражением, после чего приводим к стандартному виду
    # Результатом является лист номеров, который выводится в консоль

    print(format_phones(get_phones(get_page(URL))))
