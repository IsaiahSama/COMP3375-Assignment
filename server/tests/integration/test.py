from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Constants

BASE_URL = "http://127.0.0.1:8000"

LOGIN_PAGE_URL = BASE_URL + "/login"

driver = webdriver.Edge()

driver.get(LOGIN_PAGE_URL)

email_input = driver.find_element(By.ID, "email")

email_input.send_keys("sample@mail.com")

password_input = driver.find_element(By.ID, "password")
password_input.send_keys("Short")

driver.find_element(By.ID, "submit").click()

print("Checking Credentials")
assert driver.find_element(By.ID, "errorMessage").text == "Invalid Credentials"

print("Success!")

_ = input()

driver.close()
