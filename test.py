from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

# Function to load test data from JSON file
def load_test_data():
    with open('test/test_data.json') as f:
        data = json.load(f)
    return data

# Function to compare data in UI table with expected data
def compare_data(expected_data, actual_data):
    # Convert age values in actual data to integers
    for item in actual_data:
        item['age'] = int(item['age'])
        
    assert expected_data == actual_data, "Data does not match!"

# Load test data
test_data = load_test_data()
test_data_json = json.dumps(test_data)

# Set up Selenium
driver = webdriver.Chrome() # You need to have Chrome driver installed
driver.get("https://testpages.herokuapp.com/styled/tag/dynamic-table.html")

try:
    # Click on Table Data button
    table_data_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//summary[text()='Table Data']") ) 
     )
    table_data_button.click()

    # Insert data in input text box
    input_text_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//textarea[@id='jsondata']"))
    )
    input_text_box.clear()
    input_text_box.send_keys(test_data_json)

    # Click on Refresh Table button
    refresh_button = driver.find_element(By.XPATH, "//button[@id='refreshtable']")
    refresh_button.click()

    # Get table data from UI
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "dynamictable"))
    )

    # Get all rows from the table
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Initialize list to store actual data
    actual_data = []

    # Extract data from each row
    for row in rows[1:]:  # Skip the header row
        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = {
            "name": cells[0].text,
            "age": cells[1].text,
            "gender": cells[2].text
        }
        actual_data.append(row_data)
    
    print(actual_data)


    # Compare data
    compare_data(test_data, actual_data)

    # print(f"{test_data_json}-------------> {actual_data}-------------->")

finally:
    driver.quit()
