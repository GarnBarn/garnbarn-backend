from django.test import TestCase
from garnbarn_api.models import SocialObject

class TestModelSocialObject(TestCase):
    def setUp(self):
        """Create setup for SocialObject class."""
        self.social = SocialObject(social_id='U1efbc797c7174dd636c047f5ca8eba42')

    def test_social_id(self):
        """Test social id of the object."""
        self.assertEqual('U1efbc797c7174dd636c047f5ca8eba42', self.social.social_id)