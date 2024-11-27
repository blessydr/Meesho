# Generated by Django 4.2.16 on 2024-11-24 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Amazon', '0003_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='ratings_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='review_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.FloatField(default=0.0),
        ),
    ]