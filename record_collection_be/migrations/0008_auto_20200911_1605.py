# Generated by Django 3.1.1 on 2020-09-11 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('record_collection_be', '0007_auto_20200911_1550'),
    ]

    operations = [
        migrations.RenameField(
            model_name='album',
            old_name='release_year',
            new_name='release_date',
        ),
    ]
