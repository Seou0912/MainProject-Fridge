import re
from django.core.exceptions import ValidationError

class CustomPasswordValidator:
    def validate(self, password):
        if password is None:
            raise ValidationError("No password provided.")

        if not re.findall('[0-9]', password):
            raise ValidationError("The password must contain at least one digit, 0-9.")
        if not re.findall('[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("The password must contain at least one special character (!@#$%^&*(),.?\":{}|<>).")

    def get_help_text(self):
        return "Your password must contain at least one digit and one special character."