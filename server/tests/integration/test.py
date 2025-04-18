from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pymongo import MongoClient
from services.db_collections import Collections
from utils.config import config
from time import sleep



# Constants and integration test setup

BASE_URL = "http://127.0.0.1:8000"

REGISTRER_PAGE_URL = BASE_URL + "/register"
LOGIN_PAGE_URL = BASE_URL + "/login"
PROFILE_PAGE_URL = BASE_URL + "/profile"

options = webdriver.EdgeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
mongo_client = MongoClient(config.mongo_uri)
mongo_db = mongo_client[config.mongo_db_name]
user_collection  = mongo_db[Collections.USER.value]
report_collection = mongo_db[Collections.REPORT.value]

# Registration Integration Test
driver = webdriver.Edge(options=options)
driver.get(REGISTRER_PAGE_URL) #load registration page
first_name_input = driver.find_element(By.ID, "firstname") #gert
last_name_input = driver.find_element(By.ID, "lastname")
email_input = driver.find_element(By.ID, "email")
password_input = driver.find_element(By.ID, "password")

first_name_input.send_keys("John")
last_name_input.send_keys("Doe")
email_input.send_keys("JohnDoe@mail.com")
password_input.send_keys("bcJ0d^`76M<2")

driver.find_element(By.ID, "submit").click()

sleep(2)

is_user_created = user_collection.find_one({"email": "JohnDoe@mail.com"})

assert is_user_created is not None
assert is_user_created["email"] == "JohnDoe@mail.com"
assert is_user_created["first_name"] == "John"
assert is_user_created["last_name"] == "Doe"
assert is_user_created["role"] == "user"

print("User Creatinon Test Passed!")

driver.close()


#Login integration test
driver = webdriver.Edge(options=options)
driver.get(LOGIN_PAGE_URL)
email_input = driver.find_element(By.ID, "email")
password_input = driver.find_element(By.ID, "password")

sleep(2)

email_input.send_keys("JohnDoe@mail.com")
password_input.send_keys("bcJ0d^`76M<2")
driver.find_element(By.ID, "submit").click()

sleep(2)

assert driver.find_element(By.ID, "reportButton").text == "New Report"

sleep(2)

driver.get(PROFILE_PAGE_URL)

sleep(2)

assert driver.find_element(By.ID, "name").text == "John Doe"
assert driver.find_element(By.ID, "role").text == "Pothole Patroler"

print("Login Test Passed!")

driver.close()




