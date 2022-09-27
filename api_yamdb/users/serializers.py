from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

User = get_user_model()

FIELDS = (
    'username',
    'email',
    'first_name',
    'last_name',
    'bio',
    'role'
)


class UserSignUpSerializer(serializers.ModelSerializer):
    """Создание пользователя и отправка на почту кода подтверждения."""
    username = serializers.CharField()
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        """ Проверяем уникальность usernаme и email. """
        email = data['email']
        username = data['username']

        if username == 'me':
            raise serializers.ValidationError("Нельзя использовать имя me.")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "Почтовый ящик должен быть уникальным.")

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Имя должно быть уникальным.")

        return data


class UserTokenSerializer(serializers.Serializer):
    """Получение токена по коду подтверждения."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        fields = ('username', 'confirmation_code')

    def validate(self, attrs):
        """ Проверяем наличие кода подтверждения у пользователя. """
        user = get_object_or_404(User, username=attrs.get('username'))
        if user.confirmation_code != attrs.get('confirmation_code'):
            raise serializers.ValidationError("Неверный код подтверждения.")
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели User. """
    class Meta:
        model = User
        fields = FIELDS


class UserSelfSerializer(serializers.ModelSerializer):
    """ Сериализатор для объекта класса User. """
    class Meta:
        model = User
        fields = FIELDS
        read_only_fields = ('role',)
