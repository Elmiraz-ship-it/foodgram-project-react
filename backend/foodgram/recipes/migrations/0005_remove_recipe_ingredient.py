# Generated by Django 3.2.17 on 2023-02-07 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_ingredienttorecipe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='ingredient',
        ),
    ]