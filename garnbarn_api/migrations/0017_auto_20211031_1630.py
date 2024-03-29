# Generated by Django 3.2.7 on 2021-10-31 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garnbarn_api', '0016_auto_20211028_0848'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='garnbarn_api.customuser'),
        ),
        migrations.AddField(
            model_name='tag',
            name='reminder_time',
            field=models.JSONField(blank=True, default=None, null=True),
        ),
    ]
