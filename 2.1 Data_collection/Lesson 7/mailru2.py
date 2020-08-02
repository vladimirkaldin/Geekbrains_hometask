from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


client = MongoClient('localhost', 27017)
db = client['mailru2']
collection = db.mailru

options = Options()
options.add_argument('start-maximized')
driver = webdriver.Chrome(options=options)
driver.get('https://mail.ru/')
assert "Mail.ru" in driver.title

elem = driver.find_element_by_id('mailbox:login')
elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.ENTER)

elem = driver.find_element_by_id('mailbox:password')
elem.send_keys('NewPassword172')
elem.send_keys(Keys.ENTER)

time.sleep(3)

action = ActionChains(driver)

email = driver.find_element_by_css_selector('div.llc__container')
action.click(email).perform()

letter = {}

while True:
    sender = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'letter__author')))
    letter['sender'] = sender.text
    date = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'letter__date')))
    letter['date'] = date.text
    topic = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'thread__subject')))
    letter['topic'] = topic.text
    desc = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'letter-body__body')))
    letter['desc'] = desc.text

    collection.update_one({'sender': letter['sender']}, {'$set': letter}, upsert=True)
    action = ActionChains(driver)

    next_email = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'portal-menu-element_next')))
    action.click(next_email).perform()


driver.quit()
print('Письма собраны!')

