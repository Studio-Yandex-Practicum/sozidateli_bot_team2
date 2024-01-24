import re

from aiogram_forms.errors import ValidationError

from .constants import (INVALID_EMAIL_MESSAGE, INVALID_PHONE_NUMBER_MESSAGE,
                        INVALID_VOLUNTEERING_TYPE_MESSAGE, VOLUNTEERING_TYPE)


def validate_email_format(value: str):
    """Email validator.

    Exactly one "@" sign and at least one "." in the part after the @.
    """
    regex = re.compile(r'[^@]+@[^@]+\.[^@]+')
    match = regex.match(value)
    if not match:
        raise ValidationError(INVALID_EMAIL_MESSAGE, code='email')


def validate_phone_number_format(value: str):
    """Phone number validator."""
    regex = re.compile(
        r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'
    )
    match = regex.match(value)
    if not match:
        raise ValidationError(
            INVALID_PHONE_NUMBER_MESSAGE, code='phone_number'
        )


def validate_volunteering_type_field(value: str):
    """Volunteering type validator."""
    if value not in tuple(map(lambda x: x[1], VOLUNTEERING_TYPE)):
        raise ValidationError(
            INVALID_VOLUNTEERING_TYPE_MESSAGE, code='volunteering_type'
        )
