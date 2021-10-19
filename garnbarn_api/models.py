from django.db import models
from django.db.models import deletion


class Tag(models.Model):
    """Class that contain tags or subject of the users."""

    tag_name = models.CharField(max_length=200)
    tag_id = models.CharField(max_length=200)

    def get_tag_id(self):
        """Return id of the tag."""
        return self.tag_id

    def delete_tag(self):
        """Delete the tag."""
        return self.delete()

    def __str__(self):
        """Return name of the tag."""
        return self.tag_name