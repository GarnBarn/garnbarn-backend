# Generated by Django 3.2.7 on 2021-10-20 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_name', models.CharField(max_length=50)),
                ('due_date', models.DateTimeField(verbose_name='due date')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('detail', models.CharField(max_length=200)),
            ],
        ),
    ]