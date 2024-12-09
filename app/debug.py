from celery import shared_task
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import json
from django.core.serializers import serialize
from django.conf import settings

LOG_FILE = "/home/priyanshu/Documents/AIC/app/selenium_task.log"
ONCO_EMR_LINK = "https://secure12.oncoemr.com/nav/referrals?locationId=LH_Cz108527942_27"
USERNAME = "abhat@scale-healthcare.com"
PAS = settings.PASSWORD

def log_message(message):
    """Logs messages to the specified log file."""
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")


def wait_for_element_presence(driver, by, locator, timeout=20):
    """Waits for an element to be present."""
    try:
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.presence_of_element_located((by, locator)))
    except TimeoutException:
        log_message(f"Timeout waiting for element: {locator}")
        return None


@shared_task
def selenium_task(patient_id):
    from .models import Patient

    log_message(f"Starting selenium_task for patient_id: {patient_id}")
    
    # Fetch patient data
    try:
        patient = Patient.objects.get(id=patient_id)
        patient_json = serialize("json", [patient])
        patient_data = json.loads(patient_json)[0]["fields"]
        log_message(f"Patient Data: {patient_data}")
    except Exception as e:
        log_message(f"Error fetching patient data: {e}")
        return


    
    # Initialize Selenium
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # Debugging port setup

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.implicitly_wait(30)

        # Navigate to login page
        driver.get(ONCO_EMR_LINK)
        wait_for_element_presence(driver, By.XPATH, "//input[@id='Email']")
        driver.find_element(By.ID, "Email").send_keys(USERNAME)
        driver.find_element(By.ID, "Password").send_keys(PAS)
        driver.find_element(By.ID, "login-button").click()
        log_message("Login completed successfully.")

        # Navigate to demographic section
        wait_for_element_presence(driver, By.XPATH, "//h1[normalize-space()='Choose location']")
        driver.find_element(By.XPATH, "//div[@class='highlight']//div[@class='login-option']").click()
        driver.find_element(By.XPATH, '//*[@id="9"]/a[contains(text(),"Demographics")]').click()
        driver.find_element(By.ID, "ancNewPatient").click()

        # Handle iframe
        iframe_element = wait_for_element_presence(driver, By.XPATH, '//*[@id="modalIframeId0"]')
        driver.switch_to.frame(iframe_element)

        # Fill form
        driver.find_element(By.ID, "txtFirstName").send_keys(patient_data.get("first_name", ""))
        driver.find_element(By.ID, "txtLastName").send_keys(patient_data.get("last_name", ""))
        driver.find_element(By.ID, "cldrDOB_dateInput").send_keys(patient_data.get("date_of_birth", ""))
        if patient_data.get("sex") == "Male":
                radio_male = driver.find_element(By.XPATH, "//span[contains(text(), 'Male')]").click()
                print("male click")    

        elif patient_data.get("sex") == "Female":
                radio_female = driver.find_element(By.XPATH, "//span[contains(text(), 'Female')]").click()
        else:
                
            radio_unknown = driver.find_element(By.XPATH, "//span[contains(text(), 'Unknown')]").click()
        print("gender done ")
        log_message("Patient details entered.")

        # Save patient
        driver.find_element(By.XPATH, "//label[text()='Test Patient']").click()
        driver.find_element(By.ID, "btnSave").click()
        log_message("Patient saved successfully.")

    except WebDriverException as e:
        log_message(f"WebDriver error: {e}")
    finally:
        driver.quit()
