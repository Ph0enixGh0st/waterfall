# Waterfall contacts fetch
The script uses Waterfall.to API to find contacts for a list of companies.

## How to install
Using GitHub CLI:
```bash
gh repo clone Ph0enixGh0st/waterfall
```

Or download and unpack ZIP file from GIT Hub repository: https://github.com/Ph0enixGh0st/waterfall.git

# Prerequisites
Python3 should be already installed.
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```bash
pip install -r requirements.txt
```
In order to run the script you will need Waterfall.to API key and Postgresql credentials.
Waterfall.to API Key can be obtained here: https://www.waterfall.to/


Next step is to create a ".env" file in the same folder with your scripts.
Please include the following lines in your .env file and save the file:
```
DB_HOST={your host for postgresql DB}
DB_PORT={your port number for postgresql DB}
DB_USER={your username for postgresql DB}
DB_PASS={your password for postgresql DB}
DB_NAME={your database name for postgresql DB}
WATERFALL_API_KEY={your Waterfall API Key}
```

Then run database.py to initiate postgresql database.
```bash
python3 database.py
```


## How to run the main script
Replace "companies.csv" file with your own companies file in the "companies" folder, remember not to alter the file format.
The run the console command:

```bash
python3 main.py -t {your title filter expression here}
```

## Files created and database entries
After you run the script the "contacts.csv" will be created in "contacts" folder.
ALso all contacts will be added to your postgresql database.


## DDL for contacts table
```
CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    contact_linkedin_id VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    linkedin_id VARCHAR(255),
    linkedin_url VARCHAR(255),
    personal_email VARCHAR(255),
    location VARCHAR(255),
    country VARCHAR(255),
    company_id INTEGER,
    company_linkedin_id VARCHAR(255),
    company_name VARCHAR(255),
    company_domain VARCHAR(255),
    professional_email VARCHAR(255),
    mobile_phone VARCHAR(255),
    title VARCHAR(255)
);
```
