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
        EC.element_to_be_clickable((By.XPATH, '//a[@class="button closePopUp"]'))  # Replace with actual XPath
    )
    popup_close_button.click()
except:
    print("Popup not found or already closed.")

# Wait for the page to load completely
time.sleep(5)  # Adjust the sleep time as needed

# Locate the search box element using XPath and enter the text "all"
search_box = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//form/div[@id="-box"]/input'))  # Replace with actual XPath
)
search_box.send_keys("all")
search_box.send_keys(Keys.RETURN)

# Wait for the results to load
time.sleep(5)  # Adjust the sleep time as needed

# Extract data from li elements including before and after content
results = driver.find_elements(By.XPATH, '//ul/li[@class="membersListItem"]')  # Replace with actual XPath
for result in results:
    # Extract text content of the li element
    li_text = result.text
    # Extract content of the ::before pseudo-element
    before_content = driver.execute_script(
        'return window.getComputedStyle(arguments[0], ":before").getPropertyValue("content");', result)
    # Extract content of the ::after pseudo-element
    after_content = driver.execute_script(
        'return window.getComputedStyle(arguments[0], ":after").getPropertyValue("content");', result)

    print("LI Text:", li_text)
    print("::before content:", before_content)
    print("::after content:", after_content)
    print("--------")

# Close the driver
driver.quit()
