# Job Preferences (common across all portals)
JOB_PREFERENCES = {
    "keywords": ["Software Engineer", "Python Developer", "Backend Developer"],
    "location": "India",
    "experience_level": ["Entry level", "Mid-Senior level"],
    "job_type": ["Full-time"],
    "remote": True,
    "max_applications_per_day": 10
}

# Portal-specific settings
PORTAL_SETTINGS = {
    "linkedin": {
        "enabled": True,
        "easy_apply": True,
        "credentials": {
            "email": "",
            "password": ""
        }
    },
    "indeed": {
        "enabled": True,
        "credentials": {
            "email": "",
            "password": ""
        }
    },
    "naukri": {
        "enabled": True,
        "credentials": {
            "email": "",
            "password": ""
        }
    },
    "monster": {
        "enabled": True,
        "credentials": {
            "email": "",
            "password": ""
        }
    }
}

# Resume details
RESUME_DETAILS = {
    "name": "",
    "phone": "",
    "email": "",
    "resume_path": "resume.pdf",
    "cover_letter_path": "cover_letter.txt",
    "current_company": "",
    "current_designation": "",
    "total_experience": "",
    "current_ctc": "",
    "expected_ctc": "",
    "notice_period": ""
}

# Application settings
APPLICATION_SETTINGS = {
    "headless_mode": False,
    "random_delays": True,
    "min_delay": 2,
    "max_delay": 5,
    "save_applications": True,
    "application_log_path": "applications_log.csv"
} 