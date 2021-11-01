from django.test import TestCase, testcases
from garnbarn_api.models import CustomUser

class TestCustomUserModel(TestCase):
    def setUp(self):
        """Create setup for user model."""
        self.user1 = CustomUser(name='test1')
        self.user2 = CustomUser(uid='test_uid', name='test2')

    def test_user_name(self):
        """test user name."""
        self.assertEqual('test1', self.user1.name)
        self.assertEqual('test2', self.user2.name)

    def test_user_uid(self):
        """Test user uid with specific uid."""
        self.assertEqual('test_uid', self.user2.uid)
    
    def test_user_uid_default(self):
        """Test user default uid."""
        self.assertEqual('Unknown', self.user1.uid)