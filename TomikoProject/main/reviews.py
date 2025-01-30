import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import sqlite3


def click_load_more_button(driver):
    while True:
        try:
            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.loadMoreComments'))
            )
            load_more_button.click()
            time.sleep(2)
        except Exception as e:
            break


def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def extract_review_info(block):
    user_name = block.find('span', class_='user-name').text.strip() if block.find('span', class_='user-name') else ""
    star_rating_div = block.find('div', class_='star-rating')
    if star_rating_div:
        active_div = star_rating_div.find('div', class_='active')
        if active_div and 'data-value' in active_div.attrs:
            rating = active_div['data-value']
        else:
            rating = ""
    else:
        rating = ""
    date_text = block.find('span', class_='time').text.strip() if block.find('span', class_='time') else ""
    date_match = re.search(r'\d{1,2} \w+ \d{4}', date_text)
    date = date_match.group() if date_match else ""
    return user_name, rating, date


def main():
    url = "https://www.vl.ru/lesnaja-zaimka"
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        click_load_more_button(driver)
        scroll_to_bottom(driver)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        with sqlite3.connect('C:/Users/maiia/Tomiko-trade/TomikoProject/main/cars.sqlite3') as conn:
            cursor = conn.cursor()
            review_blocks = soup.find('ul', id='CommentsList').find_all('li', attrs={'level': '0'})
            for block in review_blocks:
                user_name, rating, date = extract_review_info(block)
                if rating:
                    add_review = "INSERT INTO reviews (user_name, rating, date) VALUES (?,?,?)"
                    data_review = (user_name, rating, date)
                    try:
                        cursor.execute(add_review, data_review)
                        conn.commit()
                    except sqlite3.IntegrityError:
                        pass
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()