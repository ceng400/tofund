import hashlib
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpRequest, HttpResponse, request
from django.contrib.auth.models import User,auth
from django.contrib import messages
from . import generalform
from . models import Fund, donation
from django.db.models import Sum, Count
from django.conf import settings
from django.contrib import messages

def dashboard(request):
    funds_data = []
    all_donations = donation.objects.all()
    for a_donation in all_donations:
        total_donations = all_donations.count()
        total_amount = sum(donation.amount for donation in all_donations) 
        funds_data.append({'fund': a_donation, 'total_donations': total_donations, 'total_amount': total_amount})
    return render(request, 'dashboard/dashboard.html', {'funds_data': funds_data})

def landingpage(request):
    return render (request, 'landingpage/index.htm')

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        if password != confirmpassword:
            messages.error(request, 'Passwords do not match')
            return redirect('signups')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already used")
            return redirect('signups')
        else:
            user = User(email=email, password=password)
            user.save()
            messages.success(request, "Registration successful. Please login.")
    return redirect('signins')   # Redirect to login page if not a POST request


def signin(request):
    if request.method == "POST":
        email=request.POST['email']
        password= request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return  render(request, 'dashboard/dashboard.html')
        else:
            messages.info(request, 'Credentials invalid')
            return redirect('signins')
    else:
        return render (request, 'userauth/login.htm')
    
def donate (request):
    return render(request, 'donation/dN.html')

def start_payment(request):
    payment_form = generalform.donationform()  # Initialize the form outside of the if statement

    if request.method == 'POST':
        payment_form = generalform.donationform(request.POST)
        if payment_form.is_valid():
            fund_id = request.POST.get('fund_id')  # Assuming 'fund_id' is the ID of the associated fund
            try:
                fund_object = Fund.objects.get(pk=fund_id)  # Retrieve the fund object
            except Fund.DoesNotExist:
                return render(request, 'donation/initiate_payment.html', {'payment_form': payment_form})
            else:
                save_payment = payment_form.save(commit=False)
                save_payment.fund = fund_object
                save_payment.save()
                return render(request, 'donation/start_payment.html', {'save_payment': save_payment, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
    else:
        payment_form = generalform.donationform()  # Assign the form again when request method is not POST

    return render(request, 'donation/initiate_payment.html', {'payment_form': payment_form})



def verify_payment(request: HttpRequest, ref:str) -> HttpResponse:
    Donation = get_object_or_404(donation, ref=ref)
    verified = Donation.verify_payment()
    if verified:
        messages.success(request, 'verification successful')
    else:
        messages.error(request, 'verification failed')    
    return redirect('landingpage')

def start_fund(request):
    if request.method == 'POST':
        startfundform = generalform.FundForm(request.POST)
        if startfundform.is_valid():
            startfundform.save()
            return redirect('dashboard')  # Redirect to the dashboard page
    else:
        startfundform = generalform.FundForm()
    return render(request, 'startfund/startfund.html', {'startfundform': startfundform})



def livefunds(request):
    funds = Fund.objects.all()  # Query all Fund objects
    funds_counter = Fund.objects.all().count()
    user = User.objects.all()
    return render(request, 'livefunds/livefunds.html', {'funds': funds, 'funds_counter': funds_counter, 'user': user})
