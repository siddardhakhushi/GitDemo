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

# Wait for the results to load
time.sleep(5)  # Adjust the sleep time as needed


# Function to check if "Load More" button is present and click it
def click_load_more():
    try:
        load_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="button load loadNextBatch"]'))
        )
        load_more_button.click()
        return True
    except:
        print("Load More button not found or already clicked.")
        return False


# Extract data from li elements including before and after content
while True:
    results = driver.find_elements(By.XPATH, '//ul/li[@class="membersListItem"]')

    for i, result in enumerate(results):
        # Click the button to reveal the additional content
        try:
            show_contact_button = result.find_element(By.XPATH, '//li/div[@class="showContactInfo"]')
            driver.execute_script("arguments[0].click();", show_contact_button)
            time.sleep(1)  # Wait for content to load
        except Exception as e:
            print("Show contact info button not found or click failed.", e)
            continue

        # Re-locate the element to avoid stale element reference
        try:
            # Re-locate the result element
            results = driver.find_elements(By.XPATH, '//ul/li[@class="membersListItem"]')
            result = results[i]
            show_contact_button = result.find_element(By.XPATH, '//li/div[@class="showContactInfo"]')

            # Extract text content of the li element
            li_text = result.text

            # Extract content of the ::before pseudo-element
            before_content = driver.execute_script(
                'return window.getComputedStyle(arguments[0], "::before").getPropertyValue("content");',
                show_contact_button)
            # Extract content of the ::after pseudo-element
            after_content = driver.execute_script(
                'return window.getComputedStyle(arguments[0], "::after").getPropertyValue("content");',
                show_contact_button)

            # Clean up the content strings
            before_content = before_content.strip('"')
            after_content = after_content.strip('"')

            print("LI Text:", li_text)
            print("::before content:", before_content if before_content != 'none' else 'None')
            print("::after content:", after_content if after_content != 'none' else 'None')
            print("--------")

        except Exception as e:
            print("Error while extracting content.", e)
            continue

    # Click "Load More" button if available, otherwise break the loop
    if not click_load_more():
        break

# Close the driver
driver.quit()
