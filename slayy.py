from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Specify the path to the ChromeDriver
path = r'C:\Program Files (x86)\chromedriver.exe'
service = Service(executable_path=path)

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=service)

# Access the website
driver.get("https://www.tcaconnect.com/Membership/Directory.html")

# Wait for the popup to appear and then close it
try:
    popup_close_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[@class="button closePopUp"]'))
    )
    popup_close_button.click()
except:
    print("Popup not found or already closed.")

# Wait for the page to load completely
time.sleep(5)  # Adjust the sleep time as needed

# Locate the search box element using XPath and enter the text "all"
search_box = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//form/div[@id="-box"]/input'))
)
search_box.send_keys("all")
search_box.send_keys(Keys.RETURN)

# Optionally, wait for a few seconds to see the results
time.sleep(5)  # Adjust the sleep time as needed

# Close the driver
driver.quit()
