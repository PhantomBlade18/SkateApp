# Generated by Django 3.1.5 on 2021-01-19 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='category',
        ),
    ]
