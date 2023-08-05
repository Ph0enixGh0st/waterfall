import os
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from my_module import Contact, Base


from dotenv import load_dotenv
load_dotenv()


class TestContactTable(unittest.TestCase):
    def setUp(self):
        # Replace the variables with your own testing database credentials
        self.TEST_DB_USER = os.environ.get("TEST_DB_USER")
        self.TEST_DB_PASS = os.environ.get("TEST_DB_PASS")
        self.TEST_DB_HOST = os.environ.get("TEST_DB_HOST")
        self.TEST_DB_PORT = os.environ.get("TEST_DB_PORT")
        self.TEST_DB_NAME = os.environ.get("TEST_DB_NAME")

        # Create a test database engine and session
        DATABASE_URL = f"postgresql://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def test_database_connection(self):
        # Test if the database connection is successful
        self.assertIsNotNone(self.session)

    def test_table_creation(self):
        # Test if the 'contact' table is created in the database
        table_exists = self.session.bind.dialect.has_table(self.session.bind, "contact")
        self.assertTrue(table_exists)

    def test_data_insertion_and_retrieval(self):
        # Test data insertion and retrieval
        new_contact = Contact(first_name="John", last_name="Doe", title="Software Engineer")
        self.session.add(new_contact)
        self.session.commit()

        retrieved_contact = self.session.query(Contact).filter_by(first_name="John").first()
        self.assertEqual(retrieved_contact.title, "Software Engineer")

    def tear_down(self):
        # Close the session and clean up the test data
        self.session.close()


if __name__ == "__main__":
    unittest.main()
