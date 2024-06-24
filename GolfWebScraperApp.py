import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get('https://lastminutegolf.co.za/')

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'searchCourseMob')))

searchInput = driver.find_element(By.ID, "searchCourseMob")
searchInput.send_keys("Cape Town")
searchInput.send_keys(Keys.RETURN)

WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'dateRangePickerFilter'))
)
datePickers = driver.find_elements(By.CLASS_NAME, 'dateRangePickerFilter')
sundayDatePicker = [datePicker for datePicker in datePickers if 'Sun' in datePicker.text]
sundayDatePicker = sundayDatePicker[0]

driver.execute_script("arguments[0].classList.add('active');", sundayDatePicker)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(sundayDatePicker))
sundayDatePicker.click()

WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'btnBookNow'))
)

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btnBookNow')))
courses = driver.find_elements(By.CLASS_NAME, 'btnBookNow')

allCourseInfo = []

for course in courses:
    course.click()
    courseName = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h4[contains(@class, '__courseNameTime')]/b"))
    ).text

    courseInfo = {}

    def extract_course_info(data_title):
        return [element.text for element in driver.find_elements(By.XPATH, f"//td[@data-title='{data_title}']")]

    courseInfo = {
        'Course Name': courseName,
        'Tee Time': extract_course_info('Tee Time'),
        'Tee': extract_course_info('Tee'),
        'Holes': extract_course_info('Holes'),
        'Rate Per Player': extract_course_info('Rate Per Player'),
        'Slots': extract_course_info('Slots'),
    }

    allCourseInfo.append(courseInfo)

    backButton = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'backSec sections mobile pt-3')]//a[contains(@class, 'btnBackList')]"))
    )
    backButton.click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btnBookNow')))
    courses = driver.find_elements(By.CLASS_NAME, 'btnBookNow')
