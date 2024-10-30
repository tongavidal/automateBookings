from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import os

email = os.environ["USERNAME"]
pwd = os.environ["PASSWORD"]

# Set up Chrome options
options = webdriver.ChromeOptions()
options.headless = False  # Change to True to run in headless mode

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

daysRange = 4 # Days reservation restriction

def denyCookies(driver):
    driver.find_element(By.CSS_SELECTOR, "#eucookielaw > div.conCookie > a:nth-child(1)").click()

current_day = datetime.now().strftime('%A')

day_action = {
    'Monday': 'WOD', # friday class
    'Tuesday': 'SUPERWOD', # saturday class
    'Wednesday': 'WOD SUNDAY', # sunday class
    'Thursday': 'WOD', # monday class
    'Friday': 'WEIGHTLIFTING', # tuesday class
    'Saturday': 'ENDURANCE', # wednesday class
    'Sunday': 'WOD' # thursday class
}

classToBook = day_action.get(current_day, "WOD")


try:
    driver.get("https://aimharder.com/login")

    denyCookies(driver)

    email_field = driver.find_element(By.NAME, "mail")
    password_field = driver.find_element(By.NAME, "pw")

    email_field.send_keys(email)
    password_field.send_keys(pwd)

    password_field.send_keys(Keys.RETURN)

    time.sleep(5)

    driver.find_element(By.CSS_SELECTOR, "#menuSwiperCon > div.swiper-wrapper > div > a.ahMenuOp.ahPicReservations").click()
    button = driver.find_element(By.ID, "nextDay")

    for i in range(daysRange):
        button.click()
        time.sleep(1)

    driver.find_element(By.CSS_SELECTOR, "#select2-filtroClases-container").click()

    input_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/span/span/span[1]/input"))
    )
    input_field.send_keys(classToBook)
    input_field.send_keys(Keys.ENTER)

    # TODO improve the book button picker
    # driver.find_element(By.CSS_SELECTOR, "#bloqueClass472329 > div.controlesClase > a:nth-child(2)").click()
    reservar_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Reservar"))
    )
    reservar_link.click()

    print(classToBook + ' was booked succesfully!')

    time.sleep(5)

finally:
    driver.quit()
