# Generated by Django 3.0.8 on 2020-08-09 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20200809_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlist',
            name='category',
            field=models.CharField(default='Not Specified', max_length=20),
        ),
        migrations.AddField(
            model_name='auctionlist',
            name='flag',
            field=models.BooleanField(default=True),
        ),
    ]
