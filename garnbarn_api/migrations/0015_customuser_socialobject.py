# Generated by Django 3.2.7 on 2021-10-28 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garnbarn_api', '0014_auto_20211025_1827'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('social_id', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('line', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='garnbarn_api.socialobject')),
            ],
        ),
    ]