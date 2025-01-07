import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import sqlite3

# Отзывы берем с вл.ру с лесной заимки (самый сок же)
url = "https://www.vl.ru/lesnaja-zaimka"

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(options=chrome_options)

driver.get(url)

# Функция для нажатия на кнопку "Загрузить еще..." (после нажатия на кнопку включается скроллер)
def click_load_more_button():
    while True:
        try:
            load_more_button = driver.find_element(By.CSS_SELECTOR, '.loadMoreComments')
            load_more_button.click()
            time.sleep(2) # Подождать, чтобы новые отзывы загрузились
        except:
            break

click_load_more_button()

# Функция для скроллинга страницы до конца
def scroll_to_bottom():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

scroll_to_bottom()


page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

conn = sqlite3.connect('C:/Users/maiia/Tomiko-trade/TomikoProject/main/cars.sqlite3')
cursor = conn.cursor()

try:
    reviews = []
    # Отзывы находятся в CommentsList, берем только с нулевым уровнем (главные)
    review_blocks = soup.find('ul', id='CommentsList').find_all('li', attrs={'level': '0'})
    for block in review_blocks:
        # Ищем имя пользователя
        user_name = block.find('span', class_='user-name').text.strip() if block.find('span', class_='user-name') else ""
        # Ищем оценку
        star_rating_div = block.find('div', class_='star-rating')
        if star_rating_div:
            active_div = star_rating_div.find('div', class_='active')
            if active_div and 'data-value' in active_div.attrs:
                rating = active_div['data-value']
            else:
                rating = ""
        else:
            rating = ""
        # Ищем дату отзыва
        date_text = block.find('span', class_='time').text.strip() if block.find('span', class_='time') else ""
        date_match = re.search(r'\d{1,2} \w+ \d{4}', date_text)
        date = date_match.group() if date_match else ""

        # Вставка данных в таблицу
        add_review = "INSERT INTO reviews (user_name, rating, date) VALUES (?,?,?)"
        data_review = (user_name, rating, date)
        cursor.execute(add_review, data_review)

    # Сохранение изменений в БД
    conn.commit()
except Exception as e:
    print(f"Произошла ошибка: {e}")
finally:
    cursor.close()
    conn.close()

    driver.quit()
