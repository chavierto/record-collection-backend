# Generated by Django 3.1.1 on 2020-11-06 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('record_collection_be', '0008_auto_20200911_1605'),
    ]

    operations = [
        migrations.RenameField(
            model_name='artist',
            old_name='name',
            new_name='artist',
        ),
    ]