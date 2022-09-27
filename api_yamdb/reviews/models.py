from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models

User = get_user_model()


class Title(models.Model):
    """Модель для произведений."""
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.TextField(null=True)
    genre = models.ManyToManyField(
        'Genre',
        through='GenreTitle',
        related_name='title_genre'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='title_category'
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Вспомогательная модель для связи жанров и произведений."""
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.CASCADE,
        related_name='genre'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title')

    def __str__(self):
        return f'{self.genre} {self.title}'


class Genre(models.Model):
    """Модель для жанров."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель для категорий."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Слаг должен состоять из строчных и заглавных '
                    'латинских букв, цифр, дефиса или нижнего подчеркивания'
        )]
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель для отзывов."""
    text = models.TextField(
        help_text='Добавьте отзыв на произведение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        help_text='Поставьте оценку от 1 до 10',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review')
        ]

    def __str__(self):
        return f'{self.text}, {self.score}'


class Comment(models.Model):
    """Модель для комментариев к отзывам."""
    text = models.TextField(
        help_text='Доавьте комментарий'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    def __str__(self):
        return self.text
