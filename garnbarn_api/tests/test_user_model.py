from django.test import TestCase, testcases
from garnbarn_api.models import CustomUser


class TestCustomUserModel(TestCase):
    def setUp(self):
        """Create setup for user model."""
        self.user1 = CustomUser(uid='test1', line="line_id1")
        self.user2 = CustomUser(uid='test2', line="line_id2")
        self.user3 = CustomUser(line="line_id3")

    def test_user_id(self):
        """test user name."""
        self.assertEqual('test1', self.user1.uid)
        self.assertEqual('test2', self.user2.uid)

    def test_user_line(self):
        """Test user uid with specific uid."""
        self.assertEqual('line_id1', self.user1.line)
        self.assertEqual('line_id2', self.user2.line)
