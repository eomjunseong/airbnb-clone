# Generated by Django 2.2.5 on 2021-04-28 02:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0009_auto_20210427_1338'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='guest',
            new_name='guests',
        ),
    ]
