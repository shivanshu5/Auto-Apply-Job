from job_portal_base import JobPortalBase
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import config
import logging

class LinkedInPortal(JobPortalBase):
    def __init__(self):
        super().__init__()
        
    def login(self):
        try:
            self.driver.get("https://www.linkedin.com/login")
            self.random_delay()
            
            # Check if already logged in
            try:
                self.driver.find_element(By.CSS_SELECTOR, "nav.global-nav")
                logging.info("Already logged in to LinkedIn")
                return True
            except NoSuchElementException:
                pass
            
            # Enter email
            email_field = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
            email_field.send_keys(config.PORTAL_SETTINGS["linkedin"]["credentials"]["email"])
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(config.PORTAL_SETTINGS["linkedin"]["credentials"]["password"])
            
            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # Wait for login to complete
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "nav.global-nav")))
            self.random_delay()
            return True
        except Exception as e:
            logging.error(f"LinkedIn login failed: {str(e)}")
            return False
            
    def search_jobs(self):
        try:
            self.driver.get("https://www.linkedin.com/jobs")
            self.random_delay()
            
            # Handle cookie consent if present
            try:
                cookie_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-tracking-control-name='accept-cookie-banner']")
                cookie_button.click()
                self.random_delay()
            except NoSuchElementException:
                pass
            
            # Enter search keywords
            search_field = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[aria-label='Search by title, skill, or company']")
            ))
            search_field.clear()
            search_field.send_keys(" ".join(config.JOB_PREFERENCES["keywords"]))
            
            # Enter location
            location_field = self.driver.find_element(
                By.CSS_SELECTOR, "input[aria-label='City, state, or zip code']"
            )
            location_field.clear()
            location_field.send_keys(config.JOB_PREFERENCES["location"])
            
            # Click search button
            search_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            search_button.click()
            
            # Wait for search results
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.job-card-container")))
            self.random_delay()
            return True
        except Exception as e:
            logging.error(f"LinkedIn job search failed: {str(e)}")
            return False
            
    def apply_for_job(self, job_element):
        try:
            job_element.click()
            self.random_delay()
            
            # Get job details for logging
            job_title = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "h2.jobs-unified-top-card__job-title")
            )).text
            company = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a.jobs-unified-top-card__company-name")
            )).text
            location = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "span.jobs-unified-top-card__bullet")
            )).text
            
            if config.PORTAL_SETTINGS["linkedin"]["easy_apply"]:
                try:
                    easy_apply_button = self.wait.until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "button.jobs-apply-button")
                    ))
                    easy_apply_button.click()
                    
                    self._fill_application_form()
                    
                    submit_button = self.wait.until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "button[aria-label='Submit application']")
                    ))
                    submit_button.click()
                    
                    # Wait for application confirmation
                    self.wait.until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "div.jobs-easy-apply-content__success-message")
                    ))
                    
                    self.log_application(job_title, company, location, self.driver.current_url)
                    return True
                except TimeoutException:
                    logging.warning("Easy Apply not available for this job")
                    return False
                
        except Exception as e:
            logging.error(f"LinkedIn application failed: {str(e)}")
            return False
            
    def _fill_application_form(self):
        try:
            # Fill name if required
            name_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[aria-label='Name']")
            if name_fields:
                name_fields[0].send_keys(config.RESUME_DETAILS["name"])
            
            # Fill phone if required
            phone_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[aria-label='Phone']")
            if phone_fields:
                phone_fields[0].send_keys(config.RESUME_DETAILS["phone"])
            
            # Upload resume if required
            resume_upload = self.driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
            if resume_upload and config.RESUME_DETAILS["resume_path"]:
                resume_upload[0].send_keys(config.RESUME_DETAILS["resume_path"])
            
            self.random_delay()
        except Exception as e:
            logging.error(f"Form filling failed: {str(e)}")
            raise
            
    def run(self):
        try:
            if not self.setup_driver():
                return
                
            if not self.login():
                return
                
            if not self.search_jobs():
                return
                
            while self.applications_count < config.JOB_PREFERENCES["max_applications_per_day"]:
                job_listings = self.driver.find_elements(By.CSS_SELECTOR, "div.job-card-container")
                
                for job in job_listings:
                    if self.applications_count >= config.JOB_PREFERENCES["max_applications_per_day"]:
                        break
                        
                    if self.apply_for_job(job):
                        self.applications_count += 1
                        logging.info(f"Successfully applied for job {self.applications_count} on LinkedIn")
                        self.random_delay()
                        
                # Scroll to load more jobs
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.random_delay()
                
        except Exception as e:
            logging.error(f"An error occurred in LinkedIn portal: {str(e)}")
        finally:
            self.cleanup() 