from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import AdminOrSuperUser
from .serializers import (UserSelfSerializer, UserSerializer,
                          UserSignUpSerializer, UserTokenSerializer)
from .services import check_token, generate_token

User = get_user_model()


@api_view(['POST'])
def sign_up(request):
    """View-функция для создания пользователя
    и отправки ему на почту кода подтверждения."""
    serializer = UserSignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    user.confirmation_code = generate_token(user)

    send_mail(
        subject='Yamdb confirmation code',
        message=f'Ваш код подтверждения: {user.confirmation_code}',
        from_email=settings.AUTH_EMAIL,
        recipient_list=[user.email]
    )
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def retrieve_token(request):
    """View-функция для получения JWT-токена по коду подтверждения
    и регистрации пользователя"""
    serializer = UserTokenSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = get_object_or_404(User, username=request.data.get('username'))
        if check_token(user, request.data.get('confirmation_code')):
            access = AccessToken.for_user(user)
            return Response(
                {
                    'token': str(access)
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'confirmation_code': 'Confirmation code is invalid'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(serializer.errors)


class UsersViewSet(viewsets.ModelViewSet):
    """Вьюсет для объектов модели User."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminOrSuperUser]
    lookup_field = 'username'
    pagination_class = PageNumberPagination

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = request.user
        serializer_class = UserSelfSerializer

        if request.method == 'GET':
            serializer = serializer_class(user)
            return Response(serializer.data)

        serializer = serializer_class(user, partial=True, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)
