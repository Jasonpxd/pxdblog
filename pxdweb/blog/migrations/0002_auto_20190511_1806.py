# Generated by Django 2.0 on 2019-05-11 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='creatte_time',
            new_name='created_time',
        ),
    ]
