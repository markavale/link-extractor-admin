# Generated by Django 3.1.1 on 2021-05-27 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scraper',
            name='error_log',
        ),
        migrations.RemoveField(
            model_name='scraper',
            name='info_log',
        ),
    ]