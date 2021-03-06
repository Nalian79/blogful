import os
import unittest
from urlparse import urlparse

from werkzeug.security import generate_password_hash

# Use the test DB
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog import models
from blog.database import Base, engine, session

class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the db
        Base.metadata.create_all(engine)

        # Create an example user
        self.user = models.User(name="Alice", email="alice@example.com",
                                password=generate_password_hash("test"))
        session.add(self.user)
        session.commit()

    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

    def simulate_login(self):
        with self.client.session_transaction() as http_session:
            http_session["user_id"] = str(self.user.id)
            http_session["_fresh"] = True

    def testAddPost(self):
        self.simulate_login()

        response = self.client.post("/post/add", data={
                "title": "Test Post",
                "content": "Test Content"
                })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/")
        posts = session.query(models.Post).all()
        self.assertEqual(len(posts), 1)

        post = posts[0]
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.content, "<p>Test Content</p>\n")
        self.assertEqual(post.author, self.user)

    def testEditPost(self):
        self.simulate_login()
        self.testAddPost()
        posts = session.query(models.Post).all()
        self.assertEqual(len(posts), 1)
        # Get the post we just added.

        post = posts[0]
        # Call up the edit form
        edit_post = self.client.post("/post/" + str(post.id) + "/edit", data={
                "title": "Edited Test Post",
                "content": "Edited Test Content"
                })

        # talk to mentor about status code 200 vs 302 here
        self.assertEqual(edit_post.status_code, 200)
        posts = session.query(models.Post).all()
        post = posts[0]
        self.assertEqual(post.title, "Edited Test Post")
        self.assertEqual(post.content, "Edited Test Content")
        self.assertEqual(post.author, self.user)

    def testDeletePost(self):
        self.simulate_login()
        self.testAddPost()

        posts = session.query(models.Post).all()
        self.assertEqual(len(posts), 1)

        post = posts[0]

        rm_post = self.client.post("/post/" + str(post.id) + "/delete", data={})
        posts = session.query(models.Post).all()
        self.assertEqual(rm_post.status_code, 200)
        self.assertEqual(len(posts), 0)

if __name__ == "__main__":
    unittest.main()
