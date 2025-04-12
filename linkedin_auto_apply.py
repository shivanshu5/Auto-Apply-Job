import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import config
import os
from dotenv import load_dotenv

class LinkedInAutoApply:
    def __init__(self):
        self.driver = None
        self.wait = None
        load_dotenv()
        
    def setup_driver(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Uncomment for headless mode
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        
    def login(self):
        try:
            self.driver.get("https://www.linkedin.com/login")
            time.sleep(random.uniform(2, 4))
            
            # Enter email
            email_field = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
            email_field.send_keys(config.LINKEDIN_CREDENTIALS["email"])
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(config.LINKEDIN_CREDENTIALS["password"])
            
            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            time.sleep(random.uniform(3, 5))
            return True
        except Exception as e:
            print(f"Login failed: {str(e)}")
            return False
            
    def search_jobs(self):
        try:
            # Navigate to jobs page
            self.driver.get("https://www.linkedin.com/jobs")
            time.sleep(random.uniform(2, 4))
            
            # Enter search keywords
            search_field = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Search by title, skill, or company']")))
            search_field.send_keys(" ".join(config.JOB_PREFERENCES["keywords"]))
            
            # Enter location
            location_field = self.driver.find_element(By.CSS_SELECTOR, "input[aria-label='City, state, or zip code']")
            location_field.clear()
            location_field.send_keys(config.JOB_PREFERENCES["location"])
            
            # Click search button
            search_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            search_button.click()
            
            time.sleep(random.uniform(3, 5))
            return True
        except Exception as e:
            print(f"Job search failed: {str(e)}")
            return False
            
    def apply_for_job(self, job_element):
        try:
            job_element.click()
            time.sleep(random.uniform(2, 4))
            
            # Check if Easy Apply is available
            easy_apply_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.jobs-apply-button")))
            easy_apply_button.click()
            
            # Fill application form
            self._fill_application_form()
            
            # Submit application
            submit_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Submit application']")))
            submit_button.click()
            
            time.sleep(random.uniform(2, 4))
            return True
        except Exception as e:
            print(f"Application failed: {str(e)}")
            return False
            
    def _fill_application_form(self):
        # This is a simplified version. You'll need to customize based on your resume details
        try:
            # Fill name if required
            name_field = self.driver.find_elements(By.CSS_SELECTOR, "input[aria-label='Name']")
            if name_field:
                name_field[0].send_keys(config.RESUME_DETAILS["name"])
            
            # Fill phone if required
            phone_field = self.driver.find_elements(By.CSS_SELECTOR, "input[aria-label='Phone']")
            if phone_field:
                phone_field[0].send_keys(config.RESUME_DETAILS["phone"])
            
            # Upload resume if required
            resume_upload = self.driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
            if resume_upload and config.RESUME_DETAILS["resume_path"]:
                resume_upload[0].send_keys(os.path.abspath(config.RESUME_DETAILS["resume_path"]))
            
            time.sleep(random.uniform(1, 2))
        except Exception as e:
            print(f"Form filling failed: {str(e)}")
            
    def run(self):
        try:
            self.setup_driver()
            if not self.login():
                return
                
            if not self.search_jobs():
                return
                
            applications_count = 0
            while applications_count < config.JOB_PREFERENCES["max_applications_per_day"]:
                job_listings = self.driver.find_elements(By.CSS_SELECTOR, "div.job-card-container")
                
                for job in job_listings:
                    if applications_count >= config.JOB_PREFERENCES["max_applications_per_day"]:
                        break
                        
                    if self.apply_for_job(job):
                        applications_count += 1
                        print(f"Successfully applied for job {applications_count}")
                        time.sleep(random.uniform(5, 10))
                        
                # Scroll to load more jobs
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(2, 4))
                
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            if self.driver:
                self.driver.quit()

if __name__ == "__main__":
    auto_apply = LinkedInAutoApply()
    auto_apply.run() 