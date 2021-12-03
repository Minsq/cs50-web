from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import User, Listing, Bid, Watchlist, Comment
from .forms import ListingForm, CommentForm # BidForm

from django.utils import timezone

def index(request):
    listings = Listing.objects.all().exclude(status__exact=False)

    return render(request, "auctions/index.html",{
        "listings": listings
    })

def categories(request, category_name):
    categories = Listing.objects.values('category').distinct().order_by().exclude(category__exact='')
    
    if category_name == 'all':
        return render(request, "auctions/categories.html",{
            "categories": categories
        })
    else:
        listings = Listing.objects.filter(category=category_name)
        return render(request, "auctions/categories.html",{
            "categories": categories,
            "category_name": category_name,
            "listings": listings
        })

@login_required(login_url="login")
def watchlist(request):
    if Watchlist.objects.filter(user=request.user).exists():
        watchlist = Watchlist.objects.get(user=request.user).item.all()
    else:
        watchlist = {}
    return render(request, "auctions/watchlist.html",{
        "listings": watchlist
    })

@login_required(login_url="login")
def create(request):
    # to get current user: use request.user
    # but do not override user
    session_user = User.objects.get(username=request.user).pk
    form = ListingForm()

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            data['creation_timestamp'] = timezone.now()
            l = Listing(seller=data['seller'], title=data['title'], description=data['description'],
                        start_price=data['start_price'], image=data['image'], category=data['category'],
                        creation_timestamp=data['creation_timestamp'])
            l.save()
            
            messages.success(request, "You have created a new Listing!")
            return HttpResponseRedirect(reverse('index'))
        else:
            current_errors = dict(form.errors)
            format_error = ""
            for k,v in current_errors.items():
                format_error += f"{k.replace('_',' ').capitalize()}: {v[0].lower().replace('.','')}; "

            messages.error(request, f"{format_error}")
            

    return render(request, "auctions/create.html",{
        'form' : form,
        'session_user': session_user
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
            messages.error(request, "Passwords must match.")
            return render(request, "auctions/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, "Username taken.")
            return render(request, "auctions/register.html")
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def get_bid_info(listing_object):
    # get the number of bids on l
    all_bids = listing_object.bids.all()
    num_bids = len(all_bids)
    if num_bids == 0:
        latest_bid_price, latest_bidder = 0, '-'
    else:
        latest_bid_price = [x.bid_price for x in all_bids][-1]
        latest_bidder = [x.buyer for x in all_bids][-1]

    return num_bids, latest_bid_price, latest_bidder

@login_required(login_url="login")
def bid(request, product_id):

    # get listing details l
    # l = get_object_or_404(Listing, pk=product_id)
    l = Listing.objects.get(pk=product_id)

    # get bid information
    num_bids, latest_bid_price, latest_bidder = get_bid_info(listing_object=l)

    # add details to a separate dict
    bid_dict = {}
    bid_dict['num_bids'] = num_bids
    bid_dict['latest_bid_price'] = latest_bid_price
    bid_dict['latest_bidder'] = latest_bidder

    # get comment form and get comments
    comment_form = CommentForm()
    comments = Comment.objects.filter(product=l)

    # get watchlist status
    if Watchlist.objects.filter(user=request.user, item=product_id).exists():
        on_watchlist = True
    else:
        on_watchlist = False
    
    # for a post request, add a new bid
    if request.method == "POST":
        
        bid_timestamp = timezone.now()
        # check if bid price is greater than the current bid
        bid_price = request.POST["bid_price"]
        try: 
            bid_price = float(bid_price)

        except ValueError:
            messages.error(request, "You have entered an invalid value.")
            return HttpResponseRedirect(reverse('bid', args=(product_id,)))

        if bid_price <= latest_bid_price or bid_price < l.start_price:
            messages.error(request, "Bid price is too low.")
            return HttpResponseRedirect(reverse('bid', args=(product_id,)))

        else:
            # buyer id - is the person in session
            buyer_id = User.objects.get(username=request.user).pk
            # finding the buyer based on buyer_id
            buyer = User.objects.get(pk = buyer_id)

            # save the bid
            b = Bid(buyer=buyer, product=l, bid_price=bid_price, bid_timestamp=bid_timestamp)
            b.save()

            messages.success(request, "You have successfully bidded!")
            return HttpResponseRedirect(reverse('bid', args=(product_id,)))
        
    
    return render(request, 'auctions/bid.html',{
        'listing': l,
        'bid_dict': bid_dict,
        'on_watchlist': on_watchlist,
        'comment_form': comment_form,
        'comments': comments
    })

def add_to_watchlist(request, product_id):
    person = User.objects.get(id = request.user.id)
    item_to_save = get_object_or_404(Listing, pk=product_id)

    # Get the user watchlist or create it if it doesn't exists - object
    user_list, is_created = Watchlist.objects.get_or_create(user=request.user)
    
    # check if item existed in watchlist - queryset
    if Watchlist.objects.filter(user=person, item=item_to_save).exists():
        user_list.item.remove(item_to_save)
        messages.warning(request, "Removed from watchlist.")
    else:
        
        user_list.item.add(item_to_save)

        # watchlist.save()
        messages.success(request, "Added to watchlist.")
    return HttpResponseRedirect(reverse('bid', args=(product_id,)))

def close_auction(request, product_id):
    if request.method=="POST":
        # get listing object
        l = get_object_or_404(Listing, pk=product_id)
        # change status to inactive/False
        l.status = False
        # get bid info
        num_bids, latest_bid_price, latest_bidder = get_bid_info(listing_object=l)
        if num_bids > 0:
            l.winner = latest_bidder
        else: 
            l.winner = None
        l.save()
        return HttpResponseRedirect(reverse('bid', args=(product_id,)))

def comment(request, product_id):
    if request.method=="POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['comment_date'] = timezone.now()
            l = get_object_or_404(Listing, pk=product_id)
            c = Comment(commenter=request.user, product=l, 
                        comment=data['comment'], comment_date= data['comment_date'])
            c.save()
            messages.success(request, 'Added comment.')
        else:
            current_errors = dict(form.errors)
            messages.error(request, f"{current_errors}")
    return HttpResponseRedirect(reverse('bid',args=(product_id,)))



    
