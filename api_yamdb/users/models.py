from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = (
    ('user', 'User'),
    ('moderator', 'Moderator'),
    ('admin', 'Admin')
)


class User(AbstractUser):
    """Модель для пользователей."""
    email = models.EmailField(
        blank=False,
        max_length=254,
        unique=True
    )
    bio = models.TextField(
        help_text='Добавьте биографию пользователя',
        blank=True
    )
    role = models.TextField(
        blank=True,
        choices=ROLES,
        default='user'
    )
    confirmation_code = models.CharField(
        max_length=100,
        blank=True
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'user'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == "admin" or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == "moderator"

    @property
    def is_user(self):
        return self.role == "user"
