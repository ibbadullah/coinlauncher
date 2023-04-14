from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from usersection.models import Accounts
from adminsection.models import *
from adminsection.other_logics import *
from django.db.models import Q
from django.http import JsonResponse




# Index/home view
def indexView(request):
    promotedCoins = CoinsModel.objects.filter(is_promoted_coin="Yes",coin_status="Listed")
    todayBestCoins = todayBest(request)
    todyBestT = todayTotalBest(request)
    allTBestCoins = allTimeBest(request)
    lauchingSoonCoins = CoinsModel.objects.filter(is_coin_launched="No",coin_status="Listed").order_by('launch_date')
    return render(request,"publicsection/index.html",{"PCoins":promotedCoins,"TBCoins":todayBestCoins,"LSCoins":lauchingSoonCoins,
                                                      "AllTimeBest":allTBestCoins,"TodayTotalBest":todyBestT})


# Login View
class LoginView(View):
    def get(self,request):
        return render(request,"publicsection/login.html")

    def post(self,request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('UserDashboard')
        else:
            messages.info(request,"Invalid credentials!")
            return render(request,'publicsection/login.html',{"alert":"alert-danger"})


# Signup view.
class SignupView(View):
    def get(self, request):
        return render(request,'publicsection/signup.html')

    def post(self, request):
        fullname = request.POST['fullname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            # Checking email
            if Accounts.objects.filter(email=email).exists():
                messages.info(request,f'Sorry an account is already created on {email}. Please use another one.')
                return render(request,'publicsection/signup.html',{'alert':'alert-warning'})
            else:
                # Creating user account
                user = Accounts.objects.create_user(fullname=fullname,email=email,password=password1,username=fullname)
                user.save()
                login(request,user)
                return redirect('UserDashboard')
        else:
            messages.info(request, 'Passwords are not correct!')
            return render(request, 'publicsection/signup.html', {'alert': 'alert-warning'})



# view for shill
def shillView(request):
    return render(request,'publicsection/shill.html')


# view for promotion
def promoteView(request):
    promotedCoins = CoinsModel.objects.filter(is_promoted_coin="Yes",coin_status="Listed")
    return render(request,'publicsection/promote.html',{"PCoins":promotedCoins})


# view for newletter
class NewsletterView(View):
    def get(self,request):
        return render(request,'publicsection/newsletter.html')

    def post(self,request):
        # first checking email in the db
        email = request.POST['email']
        if NewsLetterModel.objects.filter(email=email).exists():
            messages.info(request,"You have already subscribed for newsletter.")
            return redirect('NewsletterView')
        else:
            query = NewsLetterModel(email=email)
            query.save()
            messages.info(request,"You have successfully subscribed for our newsletter. Thanks for your interest!")
            return redirect('NewsletterView')


# view for session handling for vote alert box in coin details page
def checkDisplay(request):
    if request.session.has_key('display'):
        del request.session['display']
        return "block"
    else:
        return "none"

# view for coin details
def coinDetails(request,slug):
    try:
        ip = GetIp(request)
        query = CoinsModel.objects.get(coin_slug=slug,coin_status="Listed")
        impressions = ImpressionsModel.objects.filter(Coin__coin_slug=slug)
        totalCoinVotes = VotesModel.objects.filter(Coin__coin_slug=slug,vote_status='Approved').count()
        checkIpVote = VotesModel.objects.filter(user_ip=ip,vote_status='Approved',Coin__coin_slug=slug).count()
        display = checkDisplay(request)
        return render(request,'publicsection/coin-details.html',{"Coin":query,"Impressions":impressions,"TotalSingleCoinVotes":totalCoinVotes,
                                                                 "IpVote":checkIpVote,"display":display})
    except:
        return render(request,'404.html')


# coin impression submit view
@login_required(login_url="LoginView")
def submitImpression(request,slug):
    if request.method == "POST":
        cId = CoinsModel.objects.get(coin_slug=slug)
        impText = request.POST['imp_text']
        query = ImpressionsModel(User=request.user,Coin_id=cId.id,impression_text=impText)
        query.save()
        return redirect('CoinDetails',slug)
    else:
        return render(request,'404.html')



# vote submitting view
def submitVote(request,id):
    try:
        ip = GetIp(request)
        cSlug = CoinsModel.objects.get(id=id)
        if VotesModel.objects.filter(user_ip=ip,Coin_id=id).exists():
            return redirect('CoinDetails',cSlug.coin_slug)
        elif request.user.is_authenticated:
            if VotesModel.objects.filter(user_id=request.user.id,Coin_id=id).exists():
                return redirect('CoinDetails', cSlug.coin_slug)
            else:
                query = VotesModel(Coin_id=id, user_id=request.user.id, user_ip=ip)
                query.save()
                request.session['display'] = "block"
                return redirect('CoinDetails', cSlug.coin_slug)
        else:
            query = VotesModel(Coin_id=id, user_id=0, user_ip=ip)
            query.save()
            request.session['display'] = "block"
            return redirect('CoinDetails', cSlug.coin_slug)
    except:
        return render(request,'404.html')







