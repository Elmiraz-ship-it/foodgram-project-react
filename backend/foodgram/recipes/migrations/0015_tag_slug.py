# Generated by Django 3.2.17 on 2023-03-14 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0014_alter_recipe_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='slug',
            field=models.SlugField(default='test', max_length=32),
            preserve_default=False,
        ),
    ]
