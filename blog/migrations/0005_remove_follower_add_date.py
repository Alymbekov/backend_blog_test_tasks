# Generated by Django 3.1.3 on 2020-11-22 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20201122_1750'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follower',
            name='add_date',
        ),
    ]
