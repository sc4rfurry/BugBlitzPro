import unittest
from app import create_app, db
from app.models import User, Project


class TestViews(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.TestConfig")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Welcome to Bug Bounty Workflow Management System", response.data
        )

    def test_register(self):
        response = self.client.post(
            "/register",
            data={
                "username": "testuser",
                "email": "test@example.com",
                "password": "testpassword",
                "csrf_token": self.get_csrf_token(),
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Registration successful", response.data)

    def test_login_logout(self):
        # Register a user
        self.client.post(
            "/register",
            data={
                "username": "testuser",
                "email": "test@example.com",
                "password": "testpassword",
                "csrf_token": self.get_csrf_token(),
            },
        )

        # Login
        response = self.client.post(
            "/login",
            data={
                "username": "testuser",
                "password": "testpassword",
                "csrf_token": self.get_csrf_token(),
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login successful", response.data)

        # Logout
        response = self.client.get("/logout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"You have been logged out", response.data)

    def get_csrf_token(self):
        response = self.client.get("/login")
        return (
            response.data.split(b'name="csrf_token" value="')[1].split(b'"')[0].decode()
        )

    # Add more tests for projects, tools, and workflows views


if __name__ == "__main__":
    unittest.main()
