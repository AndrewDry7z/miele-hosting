import os
from django.core.exceptions import ValidationError


def validate_svg(value):
  ext = os.path.splitext(value.name)[1]
  valid_extensions = ['.svg']
  if not ext.lower() in valid_extensions:
    raise ValidationError('Flag icon must be SVG')
