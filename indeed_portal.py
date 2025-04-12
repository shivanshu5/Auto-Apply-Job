from job_portal_base import JobPortalBase
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import config

class IndeedPortal(JobPortalBase):
    def __init__(self):
        super().__init__()
        
    def login(self):
        try:
            self.driver.get("https://secure.indeed.com/account/login")
            self.random_delay()
            
            # Click sign in with email
            email_signin = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "button[data-tn-element='email_signin_button']")
            ))
            email_signin.click()
            
            # Enter email
            email_field = self.wait.until(EC.presence_of_element_located((By.ID, "signin_email")))
            email_field.send_keys(config.PORTAL_SETTINGS["indeed"]["credentials"]["email"])
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "signin_password")
            password_field.send_keys(config.PORTAL_SETTINGS["indeed"]["credentials"]["password"])
            
            # Click sign in button
            signin_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            signin_button.click()
            
            self.random_delay()
            return True
        except Exception as e:
            print(f"Indeed login failed: {str(e)}")
            return False
            
    def search_jobs(self):
        try:
            self.driver.get("https://www.indeed.com")
            self.random_delay()
            
            # Enter job title
            search_field = self.wait.until(EC.presence_of_element_located((By.ID, "text-input-what")))
            search_field.send_keys(" ".join(config.JOB_PREFERENCES["keywords"]))
            
            # Enter location
            location_field = self.driver.find_element(By.ID, "text-input-where")
            location_field.clear()
            location_field.send_keys(config.JOB_PREFERENCES["location"])
            
            # Click search button
            search_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            search_button.click()
            
            self.random_delay()
            return True
        except Exception as e:
            print(f"Indeed job search failed: {str(e)}")
            return False
            
    def apply_for_job(self, job_element):
        try:
            job_element.click()
            self.random_delay()
            
            # Switch to job details iframe if present
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            if iframes:
                self.driver.switch_to.frame(iframes[0])
            
            # Get job details for logging
            job_title = self.driver.find_element(By.CSS_SELECTOR, "h1.jobsearch-JobInfoHeader-title").text
            company = self.driver.find_element(By.CSS_SELECTOR, "div.jobsearch-CompanyInfoContainer").text
            location = self.driver.find_element(By.CSS_SELECTOR, "div.jobsearch-JobInfoHeader-subtitle").text
            
            # Click apply button
            apply_button = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "button[data-tn-element='apply-button']")
            ))
            apply_button.click()
            
            self._fill_application_form()
            
            self.log_application(job_title, company, location, self.driver.current_url)
            return True
            
        except Exception as e:
            print(f"Indeed application failed: {str(e)}")
            return False
            
    def _fill_application_form(self):
        try:
            # Fill name if required
            name_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[name='name']")
            if name_fields:
                name_fields[0].send_keys(config.RESUME_DETAILS["name"])
            
            # Fill email if required
            email_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[name='email']")
            if email_fields:
                email_fields[0].send_keys(config.RESUME_DETAILS["email"])
            
            # Fill phone if required
            phone_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[name='phone']")
            if phone_fields:
                phone_fields[0].send_keys(config.RESUME_DETAILS["phone"])
            
            # Upload resume if required
            resume_upload = self.driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
            if resume_upload and config.RESUME_DETAILS["resume_path"]:
                resume_upload[0].send_keys(config.RESUME_DETAILS["resume_path"])
            
            # Fill additional fields
            self._fill_additional_fields()
            
            # Submit application
            submit_button = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "button[type='submit']")
            ))
            submit_button.click()
            
            self.random_delay()
        except Exception as e:
            print(f"Form filling failed: {str(e)}")
            
    def _fill_additional_fields(self):
        try:
            # Fill current company if required
            company_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[name='current_company']")
            if company_fields:
                company_fields[0].send_keys(config.RESUME_DETAILS["current_company"])
            
            # Fill current designation if required
            designation_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[name='current_designation']")
            if designation_fields:
                designation_fields[0].send_keys(config.RESUME_DETAILS["current_designation"])
            
            # Fill experience if required
            experience_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[name='experience']")
            if experience_fields:
                experience_fields[0].send_keys(config.RESUME_DETAILS["total_experience"])
            
            # Fill salary if required
            salary_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[name='salary']")
            if salary_fields:
                salary_fields[0].send_keys(config.RESUME_DETAILS["expected_ctc"])
            
        except Exception as e:
            print(f"Additional fields filling failed: {str(e)}")
            
    def run(self):
        try:
            self.setup_driver()
            if not self.login():
                return
                
            if not self.search_jobs():
                return
                
            while self.applications_count < config.JOB_PREFERENCES["max_applications_per_day"]:
                job_listings = self.driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")
                
                for job in job_listings:
                    if self.applications_count >= config.JOB_PREFERENCES["max_applications_per_day"]:
                        break
                        
                    if self.apply_for_job(job):
                        self.applications_count += 1
                        print(f"Successfully applied for job {self.applications_count} on Indeed")
                        self.random_delay()
                        
                # Scroll to load more jobs
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.random_delay()
                
        except Exception as e:
            print(f"An error occurred in Indeed portal: {str(e)}")
        finally:
            if self.driver:
                self.driver.quit() 