import os

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database import import Base

from dotenv import load_dotenv



class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True)
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