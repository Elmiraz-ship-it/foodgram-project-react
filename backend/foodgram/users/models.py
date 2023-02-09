from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField('Username', max_length=150, unique=True)
    email = models.EmailField('Email', max_length=255, unique=True)
    first_name = models.CharField('Имя', max_length=150, blank=True, null=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    def __str__(self) -> str:
        return f'{self.username}:{self.email}'