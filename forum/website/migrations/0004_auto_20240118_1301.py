# Generated by Django 3.1.6 on 2024-01-18 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20240118_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admins',
            name='role',
            field=models.CharField(default='Admin', max_length=20),
        ),
        migrations.AlterField(
            model_name='users',
            name='role',
            field=models.CharField(default='User', max_length=20),
        ),
    ]