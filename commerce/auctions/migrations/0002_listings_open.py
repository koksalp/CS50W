# Generated by Django 3.2.6 on 2021-09-09 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='open',
            field=models.BooleanField(default=False),
        ),
    ]