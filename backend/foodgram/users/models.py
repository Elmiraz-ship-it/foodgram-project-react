from django.db import models
from django.contrib.auth.models import AbstractUser


class Follow(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='follower')
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='following')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow'
            )
        ]


class CustomUser(AbstractUser):
    username = models.CharField('Username', max_length=150, unique=True)
    email = models.EmailField('Email', max_length=255, unique=True)
    first_name = models.CharField('Имя', max_length=150, blank=True, null=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    def __str__(self) -> str:
        return f'{self.username}:{self.email}'
    
    def new_follow(self, author):
        try:
            new = Follow(user=self, author=author)
            new.save()
            return new
        except Exception as e:
            print('follow error:', str(e))
            return None