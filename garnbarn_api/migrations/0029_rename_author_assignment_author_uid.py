# Generated by Django 3.2.7 on 2021-11-07 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garnbarn_api', '0028_auto_20211104_1010'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignment',
            old_name='author',
            new_name='author_uid',
        ),
    ]