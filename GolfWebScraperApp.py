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
import datetime

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()
driver.get('https://lastminutegolf.co.za/')

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'searchCourseMob')))

searchInput = driver.find_element(By.ID, "searchCourse")
searchInput.send_keys("Cape Town")
searchInput.send_keys(Keys.RETURN)

today = datetime.date.today()
daysUntilSunday = (6 - today.weekday()) % 7
if daysUntilSunday == 0: daysUntilSunday = 7
nextSunday = today + datetime.timedelta(days=daysUntilSunday) 

WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'ui-datepicker-calendar'))
)

xpath = f"//td[a/text()='{nextSunday.day}']"
datePickerElement = driver.find_element(By.XPATH, xpath)
datePickerElement.click()

WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'btnBookNw '))
)

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btnBookNw ')))
courses = driver.find_elements(By.CLASS_NAME, 'btnBookNw ')

allCourseInfo = []

for course in courses:
    course.click()
    courseName = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "__teeTimeClub"))
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
        EC.visibility_of_element_located((By.XPATH, "//a[contains(@class, 'btnBackList')]"))
    )
    backButton.click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btnBookNow')))
    courses = driver.find_elements(By.CLASS_NAME, 'btnBookNow')
