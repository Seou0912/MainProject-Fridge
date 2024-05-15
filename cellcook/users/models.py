from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import EmailValidator


class MyUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, nickname=None, vegetarian=False, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            nickname=nickname,
            vegetarian=vegetarian,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True, primary_key=True)
    nickname = models.CharField(max_length=20)  # 필드 이름을 'nickname'으로 수정
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        null=True,
        validators=[EmailValidator(message="Enter a valid email address.")]
    )
    password = models.CharField(max_length=100)
    vegetarian = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nickname']  # 필수 필드에 'email'과 'nickname' 추가

    def __str__(self):
        return self.username
