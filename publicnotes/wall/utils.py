import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site

from . import models


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: models.User, timestamp):
        return six.text_type(user.pk) + six.text_type(timestamp) + \
               six.text_type(user.is_active)


user_activation_token = TokenGenerator()


def get_current_domain(request):
    """
    :return: current site domain by request object
    """
    return get_current_site(request).domain
