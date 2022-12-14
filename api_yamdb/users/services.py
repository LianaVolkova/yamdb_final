from django.contrib.auth.tokens import PasswordResetTokenGenerator

GENERATOR = PasswordResetTokenGenerator()


def generate_token(user):
    """Для создания токена."""
    return GENERATOR.make_token(user)


def check_token(user, token):
    """Для проверки токена."""
    return GENERATOR.check_token(user, token)
