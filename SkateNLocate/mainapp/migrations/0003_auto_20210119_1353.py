# Generated by Django 3.1.5 on 2021-01-19 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_remove_rating_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='score',
        ),
        migrations.AddField(
            model_name='rating',
            name='overall',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='rating',
            name='popularity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='rating',
            name='surface',
            field=models.IntegerField(default=0),
        ),
    ]
