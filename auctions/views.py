from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, AuctionList, Bids, Comments, Wishlist, Notifications
import datetime


def index(request):
    if request.user.id:
        notifications_count = Notifications.objects.filter(user=request.user).count()
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
        return render(request, "auctions/index.html", {
            "listings": AuctionList.objects.all(),
            "wishlist_count": wishlist_count,
            "notifications_count": notifications_count,
            'type': "Active Listing"
        })
    return render(request, "auctions/index.html", {
        "listings": AuctionList.objects.all(),
        'type': "Active Listings",
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='login')
def list_new(request):
    notifications_count = Notifications.objects.filter(user=request.user).count()
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    if request.user.is_authenticated:
        if request.method == "POST":
            title = request.POST["title"]
            desc = request.POST["description"]
            image_url = request.POST["img_url"]
            user = request.user
            price = request.POST["price"]
            date = datetime.datetime.now()
            category = request.POST["category"]
            try:
                newlist = AuctionList.objects.create(name=title, description=desc,
                                                     user=user, image_url=image_url, price=price,
                                                     date=date, category=category)
                newlist.save()
                return render(request, "auctions/index.html", {
                    "message": "Product Successfully Added to Active Listing.",
                    'wishlist_count': wishlist_count,
                })
            except:
                return render(request, 'auctions/error.html', {
                    'message': "Sorry,\n Unexpected Error Occurred",
                    'wishlist_count': wishlist_count,
                })
        else:
            return render(request, "auctions/new_listing.html", {
                "wishlist_count": wishlist_count,
                "notifications_count": notifications_count
            })
    else:
        return HttpResponseRedirect(reverse("login"))


@login_required(login_url='login')
def wishlist(request):
    if request.method == "POST":
        prod_id = request.POST['prod']
        rev_url = request.POST['url']
        wished = request.POST['wish']
        prod = AuctionList.objects.get(id=prod_id)
        if wished == "Wish":
            wish = Wishlist.objects.create(user=request.user, prod=prod)
            wish.save()
        else:
            Wishlist.objects.filter(prod=prod).delete()
        return HttpResponseRedirect(rev_url)
    wish_list = Wishlist.objects.filter(user=request.user)
    notifications_count = Notifications.objects.filter(user=request.user).count()
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    return render(request, "auctions/wishlist.html", {
        'wishlist': wish_list,
        "wishlist_count": wishlist_count,
        "notifications_count": notifications_count

    })


def product(request, prod_id):
    prod = AuctionList.objects.get(id=prod_id)
    owner = prod.user
    flag = False
    if owner == request.user:
        flag = True
    highest_bid = prod.item_bids.all().order_by('-bid')
    if len(highest_bid) == 0:
        highest_bid = prod.price + 0.1
    else:
        highest_bid = highest_bid[0].bid + 0.1
    comment = Comments.objects.filter(prod=prod_id)
    if request.user.id:
        wishes = Wishlist.objects.filter(prod=prod_id, user=request.user)
        notifications_count = Notifications.objects.filter(user=request.user).count()
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
        return render(request, 'auctions/product.html', {
            'prod': prod,
            'highest_bid': highest_bid,
            'owner': flag,
            'comments': comment,
            'wishlist' : wishes,
            "wishlist_count": wishlist_count,
            "notifications_count": notifications_count,
        })
    else:
        return render(request, 'auctions/product.html', {
            'prod': prod,
            'highest_bid': highest_bid,
            'owner': flag,
            'comments': comment,
        })


def user_listings(request, username):
    id = User.objects.get(username=username)
    prod = AuctionList.objects.filter(user=id)
    if request.user.id:
        notifications_count = Notifications.objects.filter(user=request.user).count()
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
        return render(request, 'auctions/index.html', {
            'listings': prod,
            "wishlist_count": wishlist_count,
            "notifications_count": notifications_count,
            "type": f"User: {username}"
        })
    return render(request,'auctions/index.html', {
        'listings':prod,
        "type": f"User: {username}"
    })


@login_required(login_url='login')
def my_listings(request):
    notifications_count = Notifications.objects.filter(user=request.user).count()
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    return render(request, "auctions/index.html", {
        'listings': AuctionList.objects.filter(user=request.user),
        "wishlist_count": wishlist_count,
        "notifications_count": notifications_count,
        "type": "My Listing"
    })


def categories(request):
    cat = AuctionList.objects.values('category').distinct()
    if request.user.id:
        notifications_count = Notifications.objects.filter(user=request.user).count()
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
        return render(request,'auctions/categories.html', {
            'categories':cat,
            "wishlist_count": wishlist_count,
            "notifications_count": notifications_count,

        })
    return render(request, 'auctions/categories.html',{
        'categories': cat,

    })


@login_required(login_url='login')
def notifications(request):
    notifications_count = Notifications.objects.filter(user=request.user).count()
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    return render(request, 'auctions/notifications.html',{
        'notifications': reversed(Notifications.objects.filter(user=request.user)),
        "wishlist_count": wishlist_count,
        "notifications_count": notifications_count,
    })


@login_required(login_url='login')
def close_auction(request):
    if request.method == "POST":
        prod_id = request.POST["close_auction"]
        prod = AuctionList.objects.get(id=prod_id)
        user = prod.item_bids.all().order_by("-bid")
        if len(user) == 0:
            message = f"Sorry! No One Placed Any Bid on {prod.name}. "
            new= Notifications.objects.create(user=request.user, msg=message)
        else:
            message = f"Congratulations You are the highest Bidder for the product \"{prod.name}\". Please pay  {user[0].bid} to {request.user.username}"
            message2 = f"Congratulations Your Listed Product \"{prod.name}\" Got a New Master. Please Collect {user[0].bid} from {user[0].user.username}.\n" \
                       f"Thanking You for using MYBids."
            new = Notifications.objects.create(user=user[0].user, msg=message)
            new2 = Notifications.objects.create(user=request.user, msg=message2)
        new2.save()
        new.save()
        prod.delete()
        notifications_count = Notifications.objects.filter(user=request.user).count()
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    return render(request, 'auctions/my_listings.html',{
        "wishlist_count": wishlist_count,
        "notifications_count": notifications_count
    })


@login_required(login_url='login')
def comments(request):
    comment = request.POST["comment"]
    url = request.POST["url"]
    prod_id = request.POST["prod_id"]
    prod = AuctionList.objects.get(id=prod_id)
    new_comment = Comments.objects.create(comment=comment , user=request.user, prod=prod)
    new_comment.save()
    return HttpResponseRedirect(url)


@login_required(login_url='login')
def place_bid(request):
    if request.method == "POST":
        url = request.POST["url"]
        prod_id = request.POST["prod"]
        prod = AuctionList.objects.get(id=prod_id)
        bid = request.POST['bid']
        new_bid = Bids.objects.create(bid=bid, user=request.user, prod=prod)
        new_bid.save()
        return HttpResponseRedirect(url)
    else:
        return render(request,'auctions/error.html',{
            'message': "an Error Encountered!!"
        })


def category_listing(request,category):
    if request.user.id:
        notifications_count = Notifications.objects.filter(user=request.user).count()
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
        return render(request, "auctions/index.html", {
            "listings": AuctionList.objects.filter(category=category),
            "wishlist_count": wishlist_count,
            "notifications_count": notifications_count,
            'type': f"Category: {category}"
        })

    return render(request, "auctions/index.html",{
        'type': f"Category: {category}",
        "listings": AuctionList.objects.filter(category=category)

    })


