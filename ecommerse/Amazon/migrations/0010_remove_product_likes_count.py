# Generated by Django 5.1.1 on 2024-11-26 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Amazon', '0009_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='likes_count',
        ),
    ]
