'''google-chrome --remote-debugging-port=9222 --user-data-dir="C:/ChromeDebug"
[0923/174012.498841:ERROR:file_io_posix.cc(153)] open /home/priyanshu/.config/google-chrome/Crash Reports/pending/79607d14-dc68-40ce-937d-5fc3cd9bb1ac.lock: File exists (17)'''#open chrome from command
from celery import shared_task
from time import sleep
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from django.core.serializers import serialize
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException, WebDriverException
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from django.conf import settings
@shared_task
def selenium_task(patient_id):
    # Get the patient details from the database using the patient_id
    from .models import Patient

    # Define log file for debugging
    LOG_FILE = "/home/priyanshu/Documents/AIC/app/selenium_task.log"

    # Function to log messages
    def log_message(message):
        with open(LOG_FILE, "a") as log_file:
            log_file.write(f"{datetime.now()} - {message}\n")
    from webdriver_manager.chrome import ChromeDriverManager
    log_message(f"Starting selenium_task for patient_id: {patient_id}")
    patient = Patient.objects.get(id=patient_id)
    patient_json = serialize('json', [patient])
    patient_data = json.loads(patient_json)[0]  # patient_json is a list of serialized objects
    fields = patient_data['fields']
    
    # Log the patient fields
    log_message(f"Patient Fields: {fields}")

     # Extract the date_of_birth field
    date_of_birth = fields.get('date_of_birth', 'N/A')

    # Log and print the date_of_birth
    log_message(f"Patient Date of Birth: {date_of_birth}")
    print(f"Patient Date of Birth: {date_of_birth}")

    

    def format_date_string(date_string):
        # convert mm-dd-yyyy to MM/DD/YYYY
        date_parts = date_string.split('-')
        return f'{date_parts[1]}/{date_parts[2]}/{date_parts[0]}'

    def handle_alert(driver: webdriver.Chrome):
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except NoAlertPresentException:
            log_message("No alert present to handle.")
        except WebDriverException as e:
            log_message(f"WebDriverException occurred: {e}")
        except Exception as e:
            log_message(f"An unexpected exception occurred: {e}")

    def wait_for_element_presence(driver, by, locator, timeout=20):
        try:
            wait = WebDriverWait(driver, timeout)
            element = wait.until(EC.presence_of_element_located((by, locator)))
            return element
        except:
            log_message(f"Element with locator {locator} not found.")
            return None

    def is_alert_present(driver: webdriver.Chrome) -> bool:
        try:
            try:
                WebDriverWait(driver=driver,timeout=5).until(EC.alert_is_present())
            except:pass
            driver.switch_to.alert
            return True
        except NoAlertPresentException:
            return False
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # Connect to the running instance

# Initialize WebDriver and connect to the running Chrome instance
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),            options=chrome_options)
    # # Setup WebDriver in headless mode
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run in headless mode
    # chrome_options.add_argument("--disable-gpu")  # Disable GPU for headless mode
    # chrome_options.add_argument("--window-size=1920x1080")  # Set window size (optional)
    # chrome_options.add_argument("--no-sandbox")   
    # driver = webdriver.Chrome(
    #     service=Service(ChromeDriverManager().install()),
    #     options=chrome_options
    # )
 
   
    

    # Create the WebDriver instance with the service and options
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    ONCO_EMR_LINK = "https://secure12.oncoemr.com/nav/referrals?locationId=LH_Cz108527942_27"
    USERNAME = "abhat@scale-healthcare.com"
    PAS = settings.PASSWORD


    try:
        
        driver.implicitly_wait(30)
        driver.get(ONCO_EMR_LINK)   

        # Login
        driver.find_element(By.XPATH, "//input[@id='Email']").send_keys(USERNAME)
        driver.find_element(By.XPATH, "//input[@id='Password']").send_keys(PAS)
        driver.find_element(By.XPATH, "//input[@id='login-button']").click()

        # Demographic Part
        wait_for_element_presence(driver, By.XPATH, "//h1[normalize-space()='Choose location']")
        driver.find_element(By.XPATH,"//div[@class='highlight']//div[@class='login-option']").click()
        driver.find_element(By.XPATH,'//*[@id="9"]/a[contains(text(),"Demographics")]').click()
        driver.find_element(By.XPATH,'//*[@id="ancNewPatient"]').click()

        # Switch to the iframe
        iframe_element = wait_for_element_presence(driver, By.XPATH, '//*[@id="modalIframeId0"]')
        driver.switch_to.frame(iframe_element)
        print("i frame done ")

        ############################################################################################################
        # Basic Demographics: New Patient
        # select the physician Default is the UID_Az86426924_1451 - Gelfand, MD, Robert
        try:
            # wait_for_element_presence(driver, By.ID, 'ddlDocsNonIE')
            # select_element = Select(driver.find_element(By.ID,'ddlDocsNonIE'))
            # select_element.select_by_value(fields.get('physician',"UID_Az86426924_1451"))
            # selected_option = select_element.first_selected_option
            # print("Selected option:", selected_option.text)
            print("fist name start ")
            driver.find_element(By.XPATH,"//input[@id='txtFirstName']").send_keys(fields.get('first_name',""))
            # driver.find_element(By.XPATH,"//input[@id='txtMiddleName']").send_keys(fields.get('middle_name',""))
            driver.find_element(By.XPATH,"//input[@id='txtLastName']").send_keys(fields.get('last_name',""))
            driver.find_element(By.XPATH,"//input[@id='cldrDOB_dateInput']").send_keys(format_date_string(fields.get('date_of_birth')))
            print("login done ")
            
            
            
            if fields.get("sex") == "Male":
                radio_male = driver.find_element(By.XPATH, "//span[contains(text(), 'Male')]").click()
                print("male click")    

            elif fields.get("sex") == "Female":
                radio_female = driver.find_element(By.XPATH, "//span[contains(text(), 'Female')]").click()
            else:
                
                radio_unknown = driver.find_element(By.XPATH, "//span[contains(text(), 'Unknown')]").click()
            print("gender done ")
        except:
            pass
    except:
        pass

    patient_test=driver.find_element(By.XPATH,"//label[text()='Test Patient']").click()
    print("petient clicked")
    save=driver.find_element(By.XPATH,"//input[@id='btnSave']").click()
    print("save ")      
         
           
           
         
        
        
