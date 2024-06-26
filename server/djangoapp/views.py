from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_review_from_cf, get_sentiment
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    if request.method == 'GET':
        return render(request, 'djangoapp/aboutus.html')


# Create a `contact` view to return a static contact page
def contact(request):
    if request.method == 'GET':
        return render(request, 'djangoapp/contact_us.html')
# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/registration.html')
    else:
        return render(request, 'djangoapp/index.html')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            pass
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)

            login(request, user)

            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/registration.html')
    elif request.method == 'GET':
        return render(request, 'djangoapp/registration.html')
    else:
        return redirect('django:index')

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://06566954.eu-gb.apigw.appdomain.cloud/api/dealership"
        dealerships = get_dealers_from_cf(url)
        dealer_name = ' '.join(dealer['full_name'] for dealer in dealerships)
        return HttpResponse(dealer_name)
        #context['dealer_names'] = dealer_names
        #return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == 'GET':
        url = 'https://06566954.eu-gb.apigw.appdomain.cloud/api/reviews'
        reviews = get_review_from_cf(url, dealerId=dealer_id)
        for review in reviews:
            sentiment = get_sentiment(review['review'])
            review['sentiment'] = sentiment
        context['reviews'] = reviews
        #context['sentiment'] = sentiment
        #reviews['sentiment'] = sentiment
        return HttpResponse(reviews)

# Create a `add_review` view to submit a review



