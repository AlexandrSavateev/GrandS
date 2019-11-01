from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class PhoneValidator(validators.RegexValidator):
    regex = r'^(\+375)(29|25|44|33)(\d{3})(\d{2})(\d{2})$'
    message = _(
        'Enter a valid phone number. This value may contain only numbers'
        ' and "+" character.'
    )
    flags = 0


phone_validators = [PhoneValidator()]
