# Generated by Django 4.2 on 2023-07-13 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='is_ready',
            field=models.BooleanField(default=False),
        ),
    ]
