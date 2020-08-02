from selenium import webdriver
from pymongo import MongoClient
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions

client = MongoClient('localhost', 27017)
db = client['mvideo']
collection = db.mvideo

options = Options()
options.add_argument('start-maximized')
driver = webdriver.Chrome(options=options)

driver.get('https://www.mvideo.ru')
assert 'М.Видео' in driver.title

try:
    bestsellers = driver.find_element_by_xpath('//div[contains(text(),"Хиты продаж")]/ancestor::div[@data-init="gtm-push-products"]')
except exceptions.NoSuchElementException:
    print('Хиты продаж не найдены')

while True:
    try:
        next_button = WebDriverWait(bestsellers, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[class="next-btn sel-hits-button-next"]')))

        driver.execute_script("$(arguments[0]).click();", next_button)
    except exceptions.TimeoutException:
        print('Сбор данных окончен')
        break

products = bestsellers.find_elements_by_css_selector('li.gallery-list-item')

item = {}
for product in products:
    item['info'] = product.find_element_by_css_selector('a.sel-product-tile-title').get_attribute('data-product-info')

    item['link'] = product.find_element_by_css_selector('a.sel-product-tile-title').get_attribute('href')

    item['name'] = product.find_element_by_css_selector('a.sel-product-tile-title').get_attribute('innerHTML')

    item['price'] = float(product.find_element_by_css_selector('div.c-pdp-price__current').get_attribute('innerHTML').replace('&nbsp;', '').replace('¤', ''))

    collection.update_one({'link': item['link']}, {'$set': item}, upsert=True)

driver.quit()