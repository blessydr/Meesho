# Generated by Django 5.1.1 on 2024-11-26 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Amazon', '0010_remove_product_likes_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='likes_count',
            field=models.IntegerField(default=0),
        ),
    ]
