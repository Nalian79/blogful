import os
import unittest
import multiprocessing
import time
from urlparse import urlparse
from werkzeug.security import generate_password_hash
from splinter import Browser

# Use the testing DB
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog import models
from blog.database import Base, engine, session

class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test setup """
        self.browser = Browser("phantomjs")

        # Drop DB if exists, Set up tables in the db
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Create an example user
        self.user = models.User(name="Alice", email="alice@example.com",
                                password=generate_password_hash("test"))

        session.add(self.user)
        session.commit()

        self.process = multiprocessing.Process(target=app.run)
        self.process.start()
        time.sleep(1)

    def tearDown(self):
        """ Test teardown """
        # Remove the tables and the data from the DB

        self.process.terminate()
        engine.dispose()
        session.close()
        Base.metadata.drop_all(engine)
        self.browser.quit()

    def testLoginCorrect(self):
        self.browser.visit("http://127.0.0.1:5000/login")
        self.browser.fill("email", "alice@example.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/")

    def testLoginIncorect(self):
        self.browser.visit("http://127.0.0.1:5000/login")
        self.browser.fill("email", "bob@example.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/login")


if __name__ == "__main__":
    unittest.main()
