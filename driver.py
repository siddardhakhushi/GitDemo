import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import threading
import time

# Specify the path to the ChromeDriver
path = r'C:\Program Files (x86)\chromedriver.exe'
service = Service(executable_path=path)

# Initialize the Chrome WebDriver with window maximized
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=service, options=options)

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
search_box.send_keys("ontario")
search_box.send_keys(Keys.RETURN)

# Wait for the results to load
time.sleep(5)  # Adjust the sleep time as needed

# Create a SQLite connection and cursor
main_conn = sqlite3.connect('scraped_data25.db')
main_cursor = main_conn.cursor()

# Create a table to store scraped data if it doesn't exist
main_cursor.execute('''CREATE TABLE IF NOT EXISTS scraped_data
             (id INTEGER PRIMARY KEY,
              name TEXT,
              website TEXT,
              address TEXT,
              phone TEXT,
              email TEXT)''')
main_conn.commit()

# Queue to hold elements to be processed
elements_queue = Queue()

# Lock for database operations
db_lock = threading.Lock()

# Function to load elements and add to the queue
def load_elements(driver, queue):
    while True:
        # Scroll down a bit
        driver.execute_script("window.scrollBy(0, 2000);")
        time.sleep(1)  # Slower scrolling to allow elements to load

        # Collect current results
        new_results = driver.find_elements(By.XPATH, '//ul/li[@class="membersListItem"]')
        for result in new_results:
            queue.put(result)

        try:
            # Check if "Load More" button is present and click it
            load_more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@class="button load loadNextBatch"]'))
            )
            load_more_button.click()
            time.sleep(10)  # Wait for new elements to load after clicking "Load More"
        except:
            # If no "Load More" button is found, break the loop
            break

# Function to process each result
def process_result(queue, db_lock):
    while True:
        result = queue.get()
        if result is None:
            break
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

            # Extract website and address information
            website = ''
            address_lines = []

            for line in li_text:
                if 'http' in line:
                    website = line
                else:
                    address_lines.append(line)

            address = ', '.join(address_lines[1:4])  # Adjust based on actual structure of the data

            # Insert the data into the SQLite table
            conn = sqlite3.connect('scraped_data25.db')
            with db_lock:
                c = conn.cursor()
                c.execute("INSERT INTO scraped_data (name, website, address, phone, email) VALUES (?, ?, ?, ?, ?)",
                          (name, website, address, phone, email))
                conn.commit()
                conn.close()

            print(f"Data inserted into SQLite: {name}, {website}, {address}, {phone}, {email}")

        except Exception as e:
            print("Error while extracting content.", e)
        finally:
            queue.task_done()

# ThreadPoolExecutor to manage loading and processing in parallel
with ThreadPoolExecutor(max_workers=10) as executor:
    # Start the element loader
    executor.submit(load_elements, driver, elements_queue)

    # Start the processing threads
    for _ in range(8):
        executor.submit(process_result, elements_queue, db_lock)

# Wait for all tasks to be done
elements_queue.join()

# Signal processing threads to exit
for _ in range(8):
    elements_queue.put(None)

# Close the main SQLite connection
main_conn.close()

# Close the driver
driver.quit()
