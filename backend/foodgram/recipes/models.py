from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import CustomUser as User


class Tag(models.Model):
    name = models.CharField(max_length=32, verbose_name='Название')
    color = models.CharField(max_length=32, verbose_name='Цвет')
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name
        

class Ingredient(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    measurement_unit = models.CharField(
        max_length=32,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class IngredientToRecipe(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='to_recipe',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='to_recipe',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, 'Количество не может быть меньше 1'),
            MaxValueValidator(2000, 'Количество не может быть больше 2000')
        ],
        verbose_name='Количество'
    )


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(max_length=255, verbose_name='Название')
    text = models.TextField(
        verbose_name='Описание'
    )
    cooking_time = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, 'Время приготовления не может быть меньше 1 мин'),
            MaxValueValidator(2000, 'Время приготовления не может быть больше 2000 мин')
        ],
        verbose_name='Время приготовления, мин.'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name='Теги'
    )
    image = models.ImageField(
        upload_to='images/',
        null=True,
        blank=True,
        verbose_name='Изображение'
    )
    
 
    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name
