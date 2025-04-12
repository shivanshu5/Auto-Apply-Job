from linkedin_portal import LinkedInPortal
from indeed_portal import IndeedPortal
import config
import time
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Set up logging
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, f"job_application_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

def run_portal(portal_class, portal_name):
    try:
        if config.PORTAL_SETTINGS[portal_name]["enabled"]:
            logging.info(f"Starting {portal_name} portal...")
            portal = portal_class()
            portal.run()
            logging.info(f"Completed {portal_name} portal")
        else:
            logging.info(f"{portal_name} portal is disabled")
    except Exception as e:
        logging.error(f"Error in {portal_name} portal: {str(e)}")

def main():
    try:
        logging.info("Starting job application automation...")
        
        # Create a thread pool for parallel execution
        with ThreadPoolExecutor(max_workers=len(config.PORTAL_SETTINGS)) as executor:
            # Submit portal tasks
            futures = []
            if config.PORTAL_SETTINGS["linkedin"]["enabled"]:
                futures.append(executor.submit(run_portal, LinkedInPortal, "linkedin"))
            if config.PORTAL_SETTINGS["indeed"]["enabled"]:
                futures.append(executor.submit(run_portal, IndeedPortal, "indeed"))
            
            # Wait for all tasks to complete
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"Error in portal execution: {str(e)}")
        
        logging.info("Job application automation completed")
        
    except Exception as e:
        logging.error(f"Fatal error in main application: {str(e)}")
    finally:
        logging.info("Application logs saved to: " + log_file)

if __name__ == "__main__":
    main() 