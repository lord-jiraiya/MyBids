# Generated by Django 3.0.8 on 2020-08-22 06:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_notifications'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlist',
            name='flag',
        ),
        migrations.RemoveField(
            model_name='auctionlist',
            name='sold_to',
        ),
    ]