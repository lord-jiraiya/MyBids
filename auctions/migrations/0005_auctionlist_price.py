# Generated by Django 3.0.8 on 2020-08-08 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlist',
            name='price',
            field=models.FloatField(default=20),
            preserve_default=False,
        ),
    ]