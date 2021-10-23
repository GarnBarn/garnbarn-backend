from django.test import TestCase
from garnbarn_api.models import Tag


class TagModelTests(TestCase):
    """Create setup for Tag case."""
    def setUp(self):
        self.tag = Tag(tag_name='tag1')

    def test_get_tag_name(self):
        """Test that tag object will return tag name in string."""
        self.assertEqual('tag1', str(self.tag))