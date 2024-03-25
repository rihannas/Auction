from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category, Bid, Comment


def index(request):
    if request.method == 'POST':
        category_name = request.POST['category']
        if category_name != 'all':
            categories = Category.objects.all()
            category = Category.objects.get(title=category_name)
            listings = Listing.objects.filter(isActive=True, category=category)
        else:
            listings = Listing.objects.filter(isActive=True)
            categories = Category.objects.all()
    else:
        listings = Listing.objects.filter(isActive=True)
        categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        'listings': listings,
        'categories':categories
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


def create(request):
    
    if request.method == 'POST':
        owner = request.user

        bid = Bid(bid=request.POST['starting_bid'], user=owner)
        bid.save()
    
        title = request.POST['title']
        description = request.POST['description']
        starting_bid = bid
        image_url = request.POST['image_url']
        category = Category.objects.get(title=request.POST['category'])

        
        listing = Listing(title=title, owner=owner, description=description, starting_bid=starting_bid, image_url=image_url, category=category)
        listing.save()

    categories = Category.objects.all()
    return render(request, 'auctions/create.html', {
        'categories':categories
    })

def get_listing(request, pk):
    item = Listing.objects.get(pk=pk)
    comments = item.comments.all()

    if request.user in item.watchlist.all():
        inWatchlist = True
    else:
        inWatchlist = False

    if request.user == item.owner:
        isOwner = True
    else:
        isOwner = False

    if not item.isActive and item.owner == request.user:
        message = f'Congratulations! You earned {item.starting_bid.bid}'
        return render(request, 'auctions/listing.html', {
        'item': item,
        'inWatchlist': inWatchlist,
        'comments': comments,
        'closeAuc': message,
        'isOwner': isOwner
    })

    elif not item.isActive and item.starting_bid.user == request.user:
        message = 'Congratulations! You won the auctions'
        return render(request, 'auctions/listing.html', {
        'item': item,
        'inWatchlist': inWatchlist,
        'comments': comments,
        'closeAuc': message,
        'isWinner': True
    })

    return render(request, 'auctions/listing.html', {
        'item': item,
        'inWatchlist': inWatchlist,
        'comments': comments,
        'isOwner': isOwner
    })


@login_required(login_url=login_view)
def place_bid(request, pk):
    item =  Listing.objects.get(pk=pk)
    bider = request.user
    amount = request.POST['bid']
    current_bid = item.starting_bid.bid
    if current_bid < int(float(amount)):
        bid = Bid(bid=amount, user=bider)
        bid.save()
        item.starting_bid = bid
        item.save()
        message = f'Bid was updated to {amount}'
        return render(request, 'auctions/listing.html', {
        'item': item,
        'message': message,
        'update': True
    })
    else:
        message = f'Bid should be greater than {current_bid}'
        return render(request, 'auctions/listing.html', {
                'item': item,
                'message': message,
                'update': False
            })
        
def watchlist(request):
    user = request.user
    watchlistItems = user.userwatchlist.all()
    '''
    wrong: watchlistItems = Listing.objects.filter(watchlist__userwatchlist=user)
    because: this is because user is not an instance of Listing, it is an instance of User class
    '''
    return render(request, "auctions/watchlist.html", {
        'watchlistItems': watchlistItems
    })

def add_watchlist(request, pk):
    item = Listing.objects.get(pk=pk)
    user = request.user
    user.userwatchlist.add(item)
    user.save()


    '''
    This also works
    item.watchlist.add(user)
    item.save()
    '''

    return HttpResponseRedirect(reverse('listing', args=(pk, )))

def remove_watchlist(request, pk):
    item = Listing.objects.get(pk=pk)
    user = request.user
    user.userwatchlist.remove(item)
    user.save()

    return HttpResponseRedirect(reverse('listing', args=(pk, )))

@login_required(login_url=login_view)
def add_comment(request, pk):
    item = Listing.objects.get(pk=pk)
    user = request.user
    comment = request.POST['comment']
    newCom = Comment(user=user, comment=comment, listing=item)
    newCom.save()
    return HttpResponseRedirect(reverse('listing', args=(pk, )))

def close_auction(request, pk):
    item = Listing.objects.get(pk=pk)
    user = request.user
    if item.owner == user:
        item.isActive = False
        item.save()

    return HttpResponseRedirect(reverse('listing', args=(pk, )))