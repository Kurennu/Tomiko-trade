import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os
import sys
import django
from decimal import Decimal

print(sys.path)

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TomikoProject.settings')
django.setup()

from main.models import CurrencyRate

def parse_currency_rates():
    url = "https://bbr.ru/"
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        slider = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME,'swiper-wrapper'))
        )

        time.sleep(1.5)
        last_transform = driver.execute_script("return arguments[0].style.transform", slider)
        for _ in range(5):
            time.sleep(1)
            current_transform = driver.execute_script("return arguments[0].style.transform", slider)
            if current_transform != last_transform:
                time.sleep(1.5)
                last_transform = current_transform
            else:
                break

        cookie_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.css-35blby.e8810bd2'))
        )
        cookie_button.click()
        time.sleep(2)

        all_currencies_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.css-15bdcy0.erj00p22'))
        )
        all_currencies_button.click()
        time.sleep(2)

        new_all_currencies_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.eosgyhk0.css-1vpu6o1.e8810bd2'))
        )
        new_all_currencies_button.click()
        time.sleep(5)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        currency_data = {}

        currency_rows = soup.select('tr.css-16ogjuz.e23c5741')
        for row in currency_rows:
            currency_name_td = row.select_one('td.css-5nad39.e23c5747')
            if currency_name_td:
                currency_name = currency_name_td.text.split('(')[0].strip()
                if currency_name in ['CNY', 'KRW', 'JPY']:
                    price_tds = row.select('td.css-1l3akyo.e23c5747')
                    if len(price_tds) >= 2:
                        currency_rate_td = price_tds[1].select_one('span.css-1jarydd.exmh6wy0')
                        if currency_rate_td:
                            currency_rate_str = currency_rate_td.text
                            currency_rate_str = currency_rate_str.replace(',', '.')
                            try:
                                currency_rate = Decimal(currency_rate_str)
                                currency_data[currency_name] = currency_rate
                            except Decimal.InvalidOperation:
                                print(f"Не удалось преобразовать {currency_rate_str} в число для {currency_name}")

        euro_element = soup.find('span', class_='css-90qv05 e314cwc2', string='EUR')
        if euro_element:
            sell_element = euro_element.find_next('span', class_='css-14djjag exmh6wy0', string='продажа')
            if sell_element:
                euro_rate_td = sell_element.find_next('span', class_='css-11ctayd exmh6wy0')
                if euro_rate_td:
                    euro_rate_str = euro_rate_td.text
                    euro_rate_str = euro_rate_str.replace(',', '.')
                    try:
                        euro_rate = Decimal(euro_rate_str)
                        currency_data['EUR'] = euro_rate
                    except Decimal.InvalidOperation:
                        print(f"Не удалось преобразовать {euro_rate_str} в число для EUR")

        CurrencyRate.update_rates(currency_data)

        return currency_data
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    rates = parse_currency_rates()
    print("Результат:", rates)