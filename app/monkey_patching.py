import six
from rest_framework import ISO_8601
from rest_framework.fields import DateTimeField
from rest_framework.settings import api_settings


def to_representation_ext(self, value):
    if not value:
        return None

    output_format = getattr(self, 'format', api_settings.DATETIME_FORMAT)

    if output_format is None or isinstance(value, six.string_types):
        return value

    if output_format.lower() == ISO_8601:
        value = self.enforce_timezone(value)
        value = value.isoformat()
        if value.endswith('+00:00'):
            value = value[:-6] + 'Z'
        return value

    # FOR INTEGER RESULT 'DATETIME_FORMAT': '%s',
    return int(value.timestamp())

    # FOR FLOAT RESULT 'DATETIME_FORMAT': '%s.%f',
    # return value.timestamp()


DateTimeField.to_representation = to_representation_ext
