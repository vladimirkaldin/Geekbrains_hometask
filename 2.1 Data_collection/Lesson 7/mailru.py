from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def letter_to_db(letter: {}):
    client = MongoClient('localhost', 27017)
    db = client['mailru']
    collection = db.mailru
    collection.update_one({'date': letter['date']}, {'$set': letter}, upsert=True)


def scroll():
    time.sleep(2)
    emails = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'llc__container'))
    )
    action = ActionChains(driver)
    action.move_to_element(emails[-1])
    action.perform()

def letter_collector(driver):
    letter = {}
    letter['sender'] = driver.find_element_by_class_name('ll-crpt').get_attribute('title')
    letter['date'] = driver.find_element_by_css_selector('div.llc__item_date').get_attribute('title')
    letter['topic'] = driver.find_element_by_css_selector('span.llc__subject').text
    letter['desc'] = driver.find_element_by_css_selector('span.ll-sp__normal').text
    return letter

if __name__ == '__main__':
    options = Options()
    options.add_argument('start-maximized')
    driver = webdriver.Chrome(options=options)
    driver.get('https://mail.ru/')

    elem = driver.find_element_by_id('mailbox:login')
    elem.send_keys('study.ai_172@mail.ru')
    elem.send_keys(Keys.ENTER)

    elem = driver.find_element_by_id('mailbox:password')
    elem.send_keys('NewPassword172')
    elem.send_keys(Keys.ENTER)

    emails = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'llc__content'))
    )
    while True:
        emails = driver.find_elements_by_class_name('llc__container')
        last_email = emails[-1]
        for email in emails:
            letter = letter_collector(email)
            letter_to_db(letter)
        scroll()
        scrolled_emails = driver.find_elements_by_class_name('llc__container')
        last_scrolled_email = scrolled_emails[-1]
        if last_email == last_scrolled_email:
            break

    driver.quit()
    print('Письма собраны!')




