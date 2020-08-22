from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new-listing", views.list_new, name="new_listing"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("listings/<int:prod_id>", views.product, name="product"),
    path("listings/<str:username>", views.user_listings, name="user_listings"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("categories", views.categories, name='categories'),
    path("notifications",views.notifications,name="notifications"),
    path("close_auction", views.close_auction, name="close_auction"),
    path("comments", views.comments, name="comments"),
    path("place_bid", views.place_bid , name="place_bid"),
    path("categories/<str:category>",views.category_listing, name="category_listing")

]
