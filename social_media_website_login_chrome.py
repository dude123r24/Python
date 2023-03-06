# pip3 instlal selenium
# Download driver from https://chromedriver.chromium.org/downloads (version is important. And CPU architecture) (version needs to match the one installed on your computer)
# cp /Users/amitsanghvi/Downloads/chromedriver_mac64/chromedriver  /usr/local/bin

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Set the path to the ChromeDriver executable
chrome_path = "/usr/local/bin/chromedriver"

# Create a Service object with the path to the ChromeDriver executable
service = Service(chrome_path)

# Initialize the Chrome driver with the Service object
driver = webdriver.Chrome(service=service)

# Navigate to the Facebook login page, enter the email and password, and click the login button
driver.get("https://www.facebook.com/")
time.sleep(5)

# email_field = driver.find_element_by_id("email")
email_field = driver.find_element_by_name("email")
email_field.send_keys("amit2u@hotmail.com")
password_field = driver.find_element_by_id("pass")
password_field.send_keys("Sanghv.1")
login_button = driver.find_element_by_id("loginbutton")
login_button.click()

# Close the browser window
driver.quit()
