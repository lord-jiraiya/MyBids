from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint, Q


class User(AbstractUser):
    pass


class AuctionList(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()
    description = models.CharField(max_length=400)
    image_url = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    date = models.DateTimeField()
    category = models.CharField(max_length=20, default='Not Specified')

    def __str__(self):
        return f"item {self.id}:{self.name} by {self.user.username}"

    def hbid(self):
        highest=self.item_bids.order_by("-bid")
        if len(highest)==0:
            return self.price
        else:
            return highest[0].bid


class Comments(models.Model):
    prod = models.ForeignKey(AuctionList, on_delete=models.CASCADE, related_name="item_comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    comment = models.CharField(max_length=400)


class Bids(models.Model):
    prod = models.ForeignKey(AuctionList, on_delete=models.CASCADE, related_name="item_bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")
    bid = models.FloatField()

    def __str__ (self):
        return f"{self.user.username} bids {self.bid} on product {self.prod.name}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prod = models.ForeignKey(AuctionList, on_delete=models.CASCADE, related_name="whose")

    class Meta:
        unique_together = [['user', 'prod']]


class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    msg = models.CharField(max_length=1000)
