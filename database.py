import os

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv


load_dotenv()

DB_USER = os.environ["DB_USER"]
DB_PASS = os.environ["DB_PASS"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Creates an engine to connect to the PostgreSQL database
engine = create_engine(DATABASE_URL)

# Creates a base class for declarative models
Base = declarative_base()


# Defines your contact model using SQLAlchemy ORM
class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True)
    contact_linkedin_id = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    linkedin_id = Column(String(255))
    linkedin_url = Column(String(255))
    personal_email = Column(String(255))
    location = Column(String(255))
    country = Column(String(255))
    company_id = Column(Integer)
    company_linkedin_id = Column(String(255))
    company_name = Column(String(255))
    company_domain = Column(String(255))
    professional_email = Column(String(255))
    mobile_phone = Column(String(255))
    title = Column(String(255))


# Creates the table in the database
Base.metadata.create_all(engine)
