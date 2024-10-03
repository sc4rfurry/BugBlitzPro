import unittest
from app import create_app, db
from app.models import User, Project, Tool, Workflow, WorkflowStep


class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.TestConfig")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_model(self):
        user = User(username="testuser", email="test@example.com")
        user.password = "testpassword"
        db.session.add(user)
        db.session.commit()

        retrieved_user = User.query.filter_by(username="testuser").first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.email, "test@example.com")
        self.assertTrue(retrieved_user.check_password("testpassword"))

    def test_project_model(self):
        user = User(username="testuser", email="test@example.com")
        user.password = "testpassword"
        db.session.add(user)
        db.session.commit()

        project = Project(
            name="Test Project", target_url="https://example.com", user_id=user.id
        )
        db.session.add(project)
        db.session.commit()

        retrieved_project = Project.query.filter_by(name="Test Project").first()
        self.assertIsNotNone(retrieved_project)
        self.assertEqual(retrieved_project.target_url, "https://example.com")
        self.assertEqual(retrieved_project.user_id, user.id)

    # Add more tests for Tool, Workflow, and WorkflowStep models


if __name__ == "__main__":
    unittest.main()
