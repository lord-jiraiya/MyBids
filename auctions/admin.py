from django.contrib import admin
from .models import User, Bids, AuctionList, Comments, Notifications
# Register your models here.


admin.site.register(User)
admin.site.register(Bids)
admin.site.register(AuctionList)
admin.site.register(Comments)
admin.site.register(Notifications)