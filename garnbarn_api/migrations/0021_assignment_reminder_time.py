# Generated by Django 3.2.7 on 2021-10-30 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garnbarn_api', '0020_remove_assignment_reminder_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='reminder_time',
            field=models.JSONField(blank=True, default=None, null=True),
        ),
    ]
