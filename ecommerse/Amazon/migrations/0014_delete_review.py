# Generated by Django 5.1.1 on 2024-11-26 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Amazon', '0013_remove_product_rating'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Review',
        ),
    ]
