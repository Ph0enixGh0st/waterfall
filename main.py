import argparse
import csv
import os
import requests
import time

from dotenv import load_dotenv

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


def fetch_company_and_contacts(waterfall_api_key, job_ids):
    company = {}
    companies = []
    contacts = []

    for job_id in job_ids:
        watefall_url = "https://api.waterfall.to/v1/prospector"
        params = {
            "job_id": job_id,
        }
        headers = {
            "x-waterfall-api-key": waterfall_api_key,
        }

        response = requests.get(watefall_url, headers=headers, params=params)

        if response.status_code == 200:
            print(f"Successfully sent GET request for job_id: {job_id}")
            print(response.json())
            res = response.json()

            company = {
                "comp_id": res["output"]["company"]["id'],
                "comp_domain": res["output"]["company"]["domain"],
                "comp_name": res["output"]["company"]["company_name"],
                "comp_website": res["output"]["company"]["website"],
                "comp_linkedin_id": res["output"]["company"]["linkedin_id"],
                "comp_linkedin_url": res["output"]["company"]["linkedin_url"],
                "comp_linkedin_description": res["output"]["company"]["linkedin_description"],
                "comp_size": res["output"]["company"]["size"],
                "comp_linkedin_industry": res["output"]["company"]["linkedin_industry"],
                "comp_linkedin_type": res["output"]["company"]["linkedin_type"],
                "comp_linkedin_founded": res["output"]["company"]["linkedin_founded"],
                "linkedin_employees_count": res["output"]["company"]["linkedin_employees_count"],
                "linkedin_address": res["output"]["company"]["linkedin_address"],
            }
            companies.append(company)

            for employee in res["output"]["persons"]:
                contact = {
                    "id": employee["id"],
                    "first_name": employee["first_name"] if employee["first_name"] else "None",
                    "last_name": employee["last_name"] if employee["last_name"] else "None",
                    "linkedin_id": employee["linkedin_id"] if employee["linkedin_id"] else "None",
                    "linkedin_url": employee["linkedin_url"] if employee["linkedin_url"] else "None",
                    "personal_email": employee["personal_email"] if employee["personal_email"] else "None",
                    "location": employee["location"] if employee["location"] else "None",
                    "country": employee["country"] if employee["country"] else "None",
                    "company_id": employee["company_id"] if employee["company_id"] else "None",
                    "company_linkedin_id": employee["company_linkedin_id"] if employee["company_linkedin_id"] else "None",
                    "company_name": employee["company_name"] if employee["company_name"] else "None",
                    "company_domain": employee["company_domain"] if employee["company_domain"] else "None",
                    "professional_email": employee["professional_email"] if employee["professional_email"] else "None",
                    "mobile_phone": employee["mobile_phone"] if employee["mobile_phone"] else "None",
                    "title": employee["title"] if employee["title"] else "None"
                }
                contacts.append(contact)
        else:
            print(f"Failed to send GET request for job_id: {job_id}")
            print(f"Status code: {response.status_code}")
            print(response.text)

    return companies, contacts


def write_contacts_to_csv(contacts, output_file):

    fieldnames_contacts = ["id", "first_name", "last_name", "linkedin_id", "linkedin_url", "personal_email",
                            "location", "country", "company_id", "company_linkedin_id", "company_name",
                            "company_domain", "professional_email", "mobile_phone", "phone_numbers", "title"]

    try:
        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames_contacts)
            writer.writeheader()

            # Write contacts data to CSV
            for contact in contacts:
                writer.writerow(contact)
        return True
    except Exception:
        print("Could not write contacts into CSV")
        return False


def write_contacts_to_db(contacts):
    load_dotenv()

    DB_USER = os.environ["DB_USER"]
    DB_PASS = os.environ["DB_PASS"]
    DB_HOST = os.environ["DB_HOST"]
    DB_PORT = os.environ["DB_PORT"]
    DB_NAME = os.environ["DB_NAME"]

    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Creates an engine to connect to the PostgreSQL database
    engine = create_engine(DATABASE_URL)

    try:
        # Create a session to interact with the database
        Session = sessionmaker(bind=engine)
        session = Session()

        # Now you can use the session to add, query, and manipulate data in the 'contact' table
        # Example: Inserting data into the table
        for contact in contacts:
            new_contact = Contact(
                contact_linkedin_id=contact["id"],
                first_name=contact["first_name"],
                last_name=contact["last_name"],
                linkedin_id=contact["linkedin_id"],
                linkedin_url=contact["linkedin_url"],
                personal_email=contact["personal_email"],
                location=contact["location"],
                country=contact["country"],
                company_id=contact["company_id"],
                company_linkedin_id=contact["company_linkedin_id"],
                company_name=contact["company_name"],
                company_domain=contact["company_domain"],
                professional_email=contact["professional_email"],
                mobile_phone=contact["mobile_phone"],
                title=contact["title"],
            )

            session.add(new_contact)
            session.commit()

        session.close()

    finally:
        if session:
            session.close()


def send_post_request(waterfall_api_key, company_name, domain_name, title_filter):
    job_id = ""
    watefall_url = "https://api.waterfall.to/v1/prospector"

    headers = {
        "x-waterfall-api-key": waterfall_api_key,
    }

    data = {
        "company_name": company_name,
        "title_filter": title_filter,
        "domain": domain_name
    }

    response = requests.post(watefall_url, headers=headers, json=data)

    if response.status_code == 200:
        print(f"Successfully sent POST request for {company_name}")
        data = response.json()
        job_id = data["job_id"]
        print(response.json())
    else:
        print(f"Failed to send POST request for {company_name}")
        print(f"Status code: {response.status_code}")
        print(response.text)

    return job_id


def main():

    parser = argparse.ArgumentParser(description="The script fetches contacts from Waterfall API.")
    parser.add_argument("-t", "--title_filter", default="", help="Enter your title filter sequence", type=str)
    args = parser.parse_args()
    title_filter = args.title_filter

    load_dotenv()
    waterfall_api_key = os.environ["WATERFALL_API_KEY"]
    job_ids = set()
    csv_file_path = "companies/companies.csv"

    with open(csv_file_path, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row if it exists
        for row in reader:
            company_name = row[0]  # Assuming the company name is in the first column
            domain_name = row[1]    # Assuming the domain name is in the second column
            job_id = send_post_request(waterfall_api_key, company_name, domain_name, title_filter)
            job_ids.add(job_id)
            print(f"Job IDs: {job_ids}")

    # This is a walkaround 'status': 'RUNNING'
    # Can implement async fetch or backoff tactics to make it prettier, this one is just for simplicity now
    time.sleep(60)

    if job_ids:
        companies, contacts = fetch_company_and_contacts(waterfall_api_key, job_ids)
    else:
        print("No jobs were created.")

    output_file = "contacts/contacts.csv"
    write_contacts_to_csv(contacts, output_file)
    write_contacts_to_db(contacts)


if __name__ == "__main__":
    main()
