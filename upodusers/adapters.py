import re
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.exceptions import ValidationError

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email', '')
        allowed_pattern = r'^.*@up\.edu\.ph$'
        if not re.match(allowed_pattern, email):
            raise ValidationError("Social login not allowed for this email domain. Only UP mails are allowed.")


