# Multi-Portal Job Application Automation

This is an automated job application bot that works with multiple job portals including LinkedIn, Indeed, and more. It helps you apply for jobs based on your preferences across different platforms.

## Features

- Support for multiple job portals (LinkedIn, Indeed)
- Automated job search based on keywords and location
- Easy Apply functionality
- Configurable job preferences
- Automatic form filling
- Rate limiting to avoid detection
- Resume upload support
- Application logging
- Multi-threaded operation

## Supported Job Portals

1. LinkedIn
   - Easy Apply functionality
   - Profile-based applications
   - Resume upload support

2. Indeed
   - Quick Apply functionality
   - Resume upload support
   - Custom form filling

## Prerequisites

- Python 3.8 or higher
- Chrome browser installed
- Accounts on job portals
- Resume in PDF format

## Installation

1. Clone this repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Configure your settings in `config.py`:
   - Add your portal credentials
   - Set your job preferences
   - Update your resume details
   - Configure application settings

## Usage

1. Make sure your resume is in the same directory as the script
2. Run the main script:
```bash
python main.py
```

## Configuration

Edit `config.py` to customize:

### Job Preferences
- Keywords
- Location preferences
- Experience level
- Job type
- Maximum applications per day

### Portal Settings
- Enable/disable specific portals
- Portal-specific credentials
- Portal-specific preferences

### Resume Details
- Personal information
- Current employment details
- Salary expectations
- Notice period

### Application Settings
- Headless mode
- Random delays
- Application logging
- Log file path

## Important Notes

- Use this tool responsibly and don't exceed portal rate limits
- The bot includes random delays to appear more human-like
- Make sure your resume and cover letter are up to date
- Portal interfaces may change, requiring updates to the selectors
- Some portals may have additional security measures

## Logging

The application maintains two types of logs:
1. Application log (`job_application.log`): Records the overall process
2. Applications log (`applications_log.csv`): Records details of each application

## Disclaimer

This tool is for educational purposes only. Use it at your own risk. Job portals' terms of service may prohibit automated job applications.

## License

©️Shivanshu
