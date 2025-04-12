from abc import ABC, abstractmethod
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
import pandas as pd
from datetime import datetime
import config
import logging
import os

class JobPortalBase(ABC):
    def __init__(self):
        self.driver = None
        self.wait = None
        self.applications_count = 0
        self.applications_log = []
        self.max_retries = 3
        self.retry_delay = 5
        
    def setup_driver(self):
        try:
            chrome_options = Options()
            if config.APPLICATION_SETTINGS["headless_mode"]:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            # Set download directory for resumes
            download_dir = os.path.join(os.getcwd(), "downloads")
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)
            chrome_options.add_experimental_option("prefs", {
                "download.default_directory": download_dir,
                "download.prompt_for_download": False,
            })
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            return True
        except Exception as e:
            logging.error(f"Failed to setup driver: {str(e)}")
            return False
            
    def random_delay(self):
        if config.APPLICATION_SETTINGS["random_delays"]:
            delay = random.uniform(
                config.APPLICATION_SETTINGS["min_delay"],
                config.APPLICATION_SETTINGS["max_delay"]
            )
            time.sleep(delay)
            
    def retry_operation(self, operation, *args, **kwargs):
        for attempt in range(self.max_retries):
            try:
                return operation(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    logging.error(f"Operation failed after {self.max_retries} attempts: {str(e)}")
                    raise
                logging.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                time.sleep(self.retry_delay)
                
    def log_application(self, job_title, company, location, url):
        try:
            application = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "portal": self.__class__.__name__,
                "job_title": job_title,
                "company": company,
                "location": location,
                "url": url,
                "status": "Applied"
            }
            self.applications_log.append(application)
            
            if config.APPLICATION_SETTINGS["save_applications"]:
                df = pd.DataFrame(self.applications_log)
                log_path = config.APPLICATION_SETTINGS["application_log_path"]
                df.to_csv(log_path, index=False)
                logging.info(f"Application logged to {log_path}")
        except Exception as e:
            logging.error(f"Failed to log application: {str(e)}")
            
    def cleanup(self):
        try:
            if self.driver:
                self.driver.quit()
        except Exception as e:
            logging.error(f"Error during cleanup: {str(e)}")
            
    @abstractmethod
    def login(self):
        pass
        
    @abstractmethod
    def search_jobs(self):
        pass
        
    @abstractmethod
    def apply_for_job(self, job_element):
        pass
        
    @abstractmethod
    def run(self):
        pass 