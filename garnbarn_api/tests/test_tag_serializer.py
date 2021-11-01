from django.test import TestCase
from garnbarn_api.models import Tag
from garnbarn_api.serializer import CreateTagApiSerializer


class TagAPITest(TestCase):
    """Test case for Tag API."""

    def setUp(self):
        self.tag_attributes = {
            'id': 1,
            'name': "ISP",
            'author': None,
            'color': "#4285F4",
            'reminderTime': [3600, 1800],
            'subscriber': None
        }

        self.tag_object1 = Tag.objects.create(
            name='ISP',
            color='#4285F4',
            author=None,
            reminder_time=[3600, 1800]
        )

        self.serializer1 = CreateTagApiSerializer(
            instance=self.tag_object1
        )

    def test_serializer_contain_expected_tag_field(self):
        """Test that serializer have all the header."""
        data = self.serializer1.data
        self.assertEqual(set(data.keys()), set({
            'id',
            'name',
            'color',
            'author',
            'reminderTime',
            'subscriber'
        }))

    def test_tag_field_content(self):
        """Test that serializer have all the content in side the header."""
        data = self.serializer1.data
        self.assertEqual(data['id'], self.tag_attributes['id'])
        self.assertEqual(data['name'], self.tag_attributes['name'])
        self.assertEqual(data['color'], self.tag_attributes['color'])
        self.assertEqual(data['author'], self.tag_attributes['author'])
        self.assertEqual(data['reminderTime'], self.tag_attributes['reminderTime'])
        self.assertEqual(data['subscriber'], self.tag_attributes['subscriber'])
