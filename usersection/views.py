from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Accounts
from adminsection.models import CoinsModel


# user dashboard view
@login_required(login_url='LoginView')
def userDashboard(request):
    query = CoinsModel.objects.filter(User=request.user)
    return render(request,'usersection/index.html',{"Coins":query})

# user logout view
def logoutView(request):
    logout(request)
    return redirect('IndexView')


# add coin view
class UserAddCoin(View):
    def get(self,request):
        return render(request,"usersection/add-coin.html")

    def post(self,request):
        coinName = request.POST['coin_name']
        coinSymbol = request.POST['coin_symbol']
        coinDesc = request.POST['coin_desc']
        isCoinLaunched = request.POST['is_coin_launched']
        lauchDate = request.POST['launch_date']
        tokenLogoLink = request.POST['token_logo_link']
        coinPresale = request.POST['coin_presale']
        smartContract = request.POST['smart_contract']
        ethereumContract = request.POST['ethereum_contract']
        otherLinks = request.POST['other_links']
        website = request.POST['website']
        telegram = request.POST['telegram']
        twitter = request.POST['twitter']
        redit = request.POST['reddit']

        # pushing record to the db
        query = CoinsModel(User_id=request.user.id,token_name=coinName,token_symbol=coinSymbol,token_description=coinDesc,is_coin_launched=isCoinLaunched,
                           launch_date=lauchDate,token_logo_link=tokenLogoLink,presale=coinPresale,smart_chain_address=smartContract,
                           ethereum_address=ethereumContract,other_links=otherLinks,website=website,telegram=telegram,twitter=twitter,reddit=redit)
        query.save()
        if query:
            messages.info(request,"Your coin has been added successfully!")
            return redirect('UserAddCoinView')
        else:
            messages.info(request,"Something went wrong!")
            return redirect('UserAddCoinView')


# user update profile view
class UserUpdateProfile(View):
    def get(self,request):
        return render(request,'usersection/update-profile.html')

    def post(self,request):
        fullname = request.POST['fullname']
        email = request.POST['email']

        if request.user.email == email:
            # updating only name
            query = Accounts.objects.get(email=request.user.email)
            query.fullname = fullname
            query.save()
            messages.info(request, "Your profile was updated successfully!")
            return redirect('UserUpdateProfileView')
        elif Accounts.objects.filter(email=email).exists():
            messages.info(request, "Sorry the email already exist in the system.")
            return redirect('UserUpdateProfileView')
        else:
            # updating the email and name both
            query = Accounts.objects.get(email=request.user.email)
            query.email = email
            query.fullname = fullname
            query.save()
            messages.info(request, "Your profile was updated successfully!")
            return redirect('UserUpdateProfileView')



# Pending coins
@login_required(login_url="LoginView")
def pendingCoins(request):
    query = CoinsModel.objects.filter(User=request.user,coin_status="Pending")
    return render(request,'usersection/pending-coins.html',{"Coins":query})


# Pending coins
@login_required(login_url="LoginView")
def postedCoins(request):
    query = CoinsModel.objects.filter(User=request.user,coin_status="Listed")
    return render(request,'usersection/posted-coins.html',{"Coins":query})


# Pending coins
@login_required(login_url="LoginView")
def unlistedCoins(request):
    query = CoinsModel.objects.filter(User=request.user,coin_status="Un-listed")
    return render(request,'usersection/unlisted-coins.html',{"Coins":query})
