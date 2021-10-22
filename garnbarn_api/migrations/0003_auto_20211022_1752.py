# Generated by Django 3.2.7 on 2021-10-22 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garnbarn_api', '0002_auto_20211021_1219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='tag_id',
        ),
        migrations.AddField(
            model_name='assignment',
            name='tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='garnbarn_api.tag'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='tag_name',
            field=models.CharField(max_length=20),
        ),
    ]