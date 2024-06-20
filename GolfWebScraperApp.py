import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time

options = Options()
options.add_experimental_option("detach", True)

# Set up Edge browser to be automatically accessed
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)

driver.get('https://lastminutegolf.co.za/')

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'searchCourseMob')))


searchInput = driver.find_element(By.ID, "searchCourseMob" )
searchInput.send_keys("Cape Town")
searchInput.send_keys(Keys.RETURN)

courses = driver.find_elements(By.CLASS_NAME, 'btnBookNow ')

datePickers = driver.find_elements(By.CLASS_NAME, 'dateRangePickerFilter')
sundayDatePicker = [datePicker for datePicker in datePickers if 'Sun' in datePicker.text]
sundayDatePicker = sundayDatePicker[0]

driver.execute_script("arguments[0].classList.add('active');", sundayDatePicker)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(sundayDatePicker)) 
sundayDatePicker.click()

if len(courses) > 0:
    # Select the first course in the list of courses. 
    courses[0].click()

    #Wait until the li element containing 'Sun' has been loaded, then find these elements. 
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'dateRangePickerFilter'))
    )
    datePickers = driver.find_elements(By.CLASS_NAME, 'dateRangePickerFilter')
    sundayDatePicker = [datePicker for datePicker in datePickers if 'Sun' in datePicker.text]
    sundayDatePicker = sundayDatePicker[0]

    driver.execute_script("arguments[0].classList.add('active');", sundayDatePicker)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(sundayDatePicker)) 
    sundayDatePicker.click()
    #Get the appropriate information from the page 


    #Repeat for the rest of the courses in the list. 




else:
        print("No buttons found to click")