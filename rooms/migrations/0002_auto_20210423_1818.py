# Generated by Django 2.2.5 on 2021-04-23 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]