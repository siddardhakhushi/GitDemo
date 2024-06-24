import sqlite3
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

# Locate the search box element using XPath and enter the text "inc"
search_box = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//form/div[@id="-box"]/input'))
)
search_box.send_keys("inc")
search_box.send_keys(Keys.RETURN)

# Wait for the results to load
time.sleep(5)  # Adjust the sleep time as needed

# Create a SQLite connection and cursor
conn = sqlite3.connect('scraped_data7.db')
c = conn.cursor()

# Create a table to store scraped data if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS scraped_data
             (id INTEGER PRIMARY KEY,
              name TEXT,
              website TEXT,
              address TEXT,
              phone TEXT,
              email TEXT)''')

# Function to load all elements
def load_all_elements():
    while True:
        # Scroll down a bit
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2)  # Wait for new elements to load

        try:
            # Check if "Load More" button is present and click it
            load_more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@class="button load loadNextBatch"]'))
            )
            load_more_button.click()
            time.sleep(3)  # Wait for new elements to load
        except:
            # If no "Load More" button is found, break the loop
            break

# Load all elements by scrolling and clicking "Load More"
load_all_elements()

# Wait a bit to ensure all elements are loaded
time.sleep(5)

# Extract data from li elements including before and after content
results = driver.find_elements(By.XPATH, '//ul/li[@class="membersListItem"]')

for result in results:
    try:
        # Click the button to reveal the additional content
        show_contact_button = result.find_element(By.XPATH, './/div[@class="showContactInfo"]')
        driver.execute_script("arguments[0].click();", show_contact_button)
        time.sleep(1)  # Wait for content to load

        # Find the element containing the name
        name_element = result.find_element(By.XPATH, './/h4[@class="companyName name"]')
        name = name_element.text

        # Find the elements containing phone number and email address
        phone_element = result.find_element(By.CLASS_NAME, 'phoneNumber')
        email_element = result.find_element(By.CLASS_NAME, 'emailAddress')

        # Extract text content of the elements
        phone = phone_element.text
        email = email_element.text

        # Extract text content of the li element
        li_text = result.text.split('\n')

        # Extracted data assuming a structure:
        # name, website, address1, address2, address3
        website = li_text[1] if 'http' in li_text[1] else ''
        address = ', '.join(li_text[2:5])

        # Insert the data into the SQLite table
        c.execute("INSERT INTO scraped_data (name, website, address, phone, email) VALUES (?, ?, ?, ?, ?)",
                  (name, website, address, phone, email))
        conn.commit()

        print(f"Data inserted into SQLite: {name}, {website}, {address}, {phone}, {email}")

    except Exception as e:
        print("Error while extracting content.", e)
        continue

# Close the SQLite connection
conn.close()

# Close the driver
driver.quit()
