import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import sqlite3


def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


from urllib.parse import urljoin


def extract_clip_info(block, base_url):
    clip_link = block.find('a', attrs={'data-testid': 'clip-preview'})
    link = clip_link['href'] if clip_link else ""
    link = urljoin(base_url, link)
    cover_div = block.find('div', attrs={'data-testid': 'clipcard-cover'})
    cover_img = cover_div.find('img') if cover_div else None
    cover_url = cover_img['src'] if cover_img else ""
    return cover_url, link


def main():
    url = "https://vk.com/clips/tomiko_trade"
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        scroll_to_bottom(driver)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        with sqlite3.connect('C:/Users/maiia/Tomiko-trade/TomikoProject/main/cars.sqlite3') as conn:
            cursor = conn.cursor()
            clip_blocks = soup.find_all('div', attrs={'data-testid': 'grid-item'})
            for block in clip_blocks:
                cover_url, link = extract_clip_info(block, url)
                add_clip = "INSERT INTO clips (cover_url, link) VALUES (?,?)"
                data_clip = (cover_url, link)
                try:
                    cursor.execute(add_clip, data_clip)
                    conn.commit()
                except sqlite3.IntegrityError:
                    pass
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()