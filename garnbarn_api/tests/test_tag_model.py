from django.test import TestCase
from garnbarn_api.models import CustomUser, Tag


class TagModelTests(TestCase):
    """Create setup for Tag case."""

    def setUp(self):
        self.tag = Tag(name='tag1')
        self.tag2 = Tag(name='tag2', color='white', author=(
            CustomUser(uid='test')), reminder_time=[3600, 1800])

    def test_get_tag_name(self):
        """Test that tag object will return tag name in string."""
        self.assertEqual('tag1', str(self.tag))

    def test_get_tag_color(self):
        """Test tag color."""
        self.assertEqual('white', self.tag2.color)

    def test_get_tag_author(self):
        """Test that tag object can get author name."""
        self.assertIsInstance(self.tag2.author, CustomUser)

    def test_no_author(self):
        """Test tag that no author."""
        self.assertEqual(None, self.tag.author)

    def test_no_tag_clor(self):
        """Test that that has no color."""
        self.assertEqual(None, self.tag.color)

    def test_tag_with_no_reminder(self):
        """Test tag that has no reminder time."""
        self.assertEqual(None, self.tag.reminder_time)

    def test_tag_reminder(self):
        """Test tag remider."""
        self.assertEqual([3600, 1800], self.tag2.reminder_time)
