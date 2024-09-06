import time
from enum import Enum

from selenium import webdriver
# from selenium.webdriver.chrome.service import Service # for chrome
from selenium.webdriver.firefox.service import Service # for firefox
from selenium.webdriver.common.by import By


# define button id's
class Elements(Enum):
    login_page_btn = "//a[text()='Login']" # xpath

    username_field = "username" # id
    username_value = "admin"    # my value

    password_field = "password" # id
    password_value = "admin1"   # my value

    login_btn = "input.btn.btn-primary" # CSS selector

    #####################################################

    quote_class_name = 'quote' # class


def load_page(url):
    driver.get(url)
    print(driver.title)

    time.sleep(0.5) # wait to allow page load properly


# TODO: Poprawić argumety funkcji i zastosować je w funkcji
def login():
    login_page = driver.find_element(By.XPATH, Elements.login_page_btn.value)
    login_page.click()
    username = driver.find_element(By.ID, Elements.username_field.value)
    username.send_keys(Elements.username_value.value)

    password = driver.find_element(By.ID, Elements.password_field.value)
    password.send_keys(Elements.password_value.value)

    login = driver.find_element(By.CSS_SELECTOR, Elements.login_btn.value)
    login.click()


def scrape_quotes():
    quotes = []
    authors = []
    tags = []
    iterator = 1
    keep_scraping = True

    while keep_scraping:
        quote_elements = driver.find_elements(By.CLASS_NAME, Elements.quote_class_name.value)
        print(len(quote_elements))
        for quote in quote_elements:
            quotes.append(quote.find_element(By.CLASS_NAME, 'text').text)
            authors.append(quote.find_element(By.CLASS_NAME, 'author').text)
            tags.append([tag.text for tag in quote.find_elements(By.CLASS_NAME, 'tag')])
            iterator += 1
            if iterator>=10:
                keep_scraping = False # break main loop
                break # break for loop

    return quotes, authors, tags


def save2txt(data):
    quotes = data[0]
    authors = data[1]
    tags = data[2]

    with open("scraped_quotes.txt", "w") as file:
        for i in range(len(quotes)):
            file.write(f'{quotes[i]}\n')
            file.write(f'{authors[i]}\n')
            file.write(f'{tags[i]}\n')
            file.write('\n')


if __name__ == "__main__":
    try:
        #load driver
        service = Service(executable_path="geckodriver.exe")
        driver = webdriver.Firefox(service=service)
        url = 'https://quotes.toscrape.com/'

        load_page(url)
        login()
        scraped_sentences = scrape_quotes()
        save2txt(scraped_sentences)

    finally:
        driver.quit()
