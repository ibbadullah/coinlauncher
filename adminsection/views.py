from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from usersection.models import Accounts
from .models import *
from .other_logics import checkAdmin
from django.core.paginator import Paginator


'''
#############################
Admin dashboard and profile related stuff 
#############################
'''
# Admin dashboard view
@login_required(login_url="AdminLogin")
def adminDashbaordView(request):
    if checkAdmin(request) == True:
        query = CoinsModel.objects.all().order_by('-id')
        return render(request, 'adminsection/index.html', {"coins": query})
    else:
        return render(request,'404.html')



# Login View
class AdminLoginView(View):
    def get(self,request):
        return render(request,"adminsection/login.html")

    def post(self,request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email,password=password)
        if Accounts.objects.filter(email=email,is_admin=True,is_staff=True,is_superuser=True).exists():
            if user is not None:
                login(request, user)
                return redirect('AdminDashboard')
            else:
                messages.info(request, "Invalid credentials!")
                return render(request, 'adminsection/login.html', {"alert": "alert-danger"})
        else:
            messages.info(request, "Sorry only an admin can login to the system!")
            return render(request, 'adminsection/login.html', {"alert": "alert-danger"})



# admin update profile view
class AdminUpdateProfile(View):
    def get(self,request):
        if checkAdmin(request) == True:
            return render(request,'adminsection/update-profile.html')
        else:
            return render(request,'404')


    def post(self,request):
        fullname = request.POST['fullname']
        email = request.POST['email']

        if request.user.email == email:
            # updating only name
            query = Accounts.objects.get(email=request.user.email)
            query.fullname = fullname
            query.save()
            messages.info(request, "Your profile was updated successfully!")
            return redirect('UpdateAdminProfileView')
        elif Accounts.objects.filter(email=email).exists():
            messages.info(request, "Sorry the email already exist in the system.")
            return redirect('UpdateAdminProfileView')
        else:
            # updating the email and name both
            query = Accounts.objects.get(email=request.user.email)
            query.email = email
            query.fullname = fullname
            query.save()
            messages.info(request, "Your profile was updated successfully!")
            return redirect('UpdateAdminProfileView')




'''
#############################
Admin coins related stuff 
#############################
'''
# Admin view for all coins
@login_required(login_url="AdminLogin")
def adminAllCoinsView(request):
    if checkAdmin(request) == True:
        query = CoinsModel.objects.all().order_by('-id')
        paginator = Paginator(query,15)
        page = request.GET.get('page')
        query = paginator.get_page(page)
        return render(request,'adminsection/coins.html',{"Data":query})
    else:
        return render(request,'404.html')



# add coin view
class AdminAddCoin(View):
    def get(self,request):
        if checkAdmin(request) == True:
            return render(request,"adminsection/add-coin.html")
        else:
            return render(request,'404')

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
        promotedCoin = request.POST['promoted_coin']
        # pushing record to the db
        query = CoinsModel(User_id=request.user.id,token_name=coinName,token_symbol=coinSymbol,token_description=coinDesc,is_coin_launched=isCoinLaunched,
                           launch_date=lauchDate,token_logo_link=tokenLogoLink,presale=coinPresale,smart_chain_address=smartContract,
                           ethereum_address=ethereumContract,other_links=otherLinks,website=website,telegram=telegram,twitter=twitter,reddit=redit,is_promoted_coin=promotedCoin)
        query.save()
        if query:
            messages.info(request,"A new coin was added successfully!")
            return redirect('AdminAllCoins')
        else:
            messages.info(request,"Something went wrong!")
            return redirect('AdminAllCoins')



# Admin view for unlisting coin
@login_required(login_url="AdminLogin")
def unlistCoin(request,id):
    if checkAdmin(request) == True:
        try:
            query = CoinsModel.objects.get(id=id)
            query.coin_status = "Un-list"
            query.save()
            messages.info(request, f"Coin id {id} has been un-listed.")
            return redirect('AdminAllCoins')
        except:
            messages.info(request,"Something went wrong!")
            return redirect('AdminAllCoins')
    else:
        return render(request,'404.html')



# Admin view for listing coin
@login_required(login_url="AdminLogin")
def listCoin(request,id):
    if checkAdmin(request) == True:
        try:
            query = CoinsModel.objects.get(id=id)
            query.coin_status = "Listed"
            query.save()
            messages.info(request, f"Coin id {id} has been listed.")
            return redirect('AdminAllCoins')
        except:
            messages.info(request,"Something went wrong!")
            return redirect('AdminAllCoins')
    else:
        return render(request,'404.html')



# Admin view for deleting coin
@login_required(login_url="AdminLogin")
def deleteCoin(request,id):
    if checkAdmin(request) == True:
        try:
            query = CoinsModel.objects.get(id=id)
            query.delete()
            messages.info(request, f"Coin id {id} was deleted successfully.")
            return redirect('AdminAllCoins')
        except:
            messages.info(request,"Something went wrong!")
            return redirect('AdminAllCoins')
    else:
        return render(request,'404.html')



# Admin class base view for updating coin
class CoinUpdateView(View):
    def get(self,request,id):
        if checkAdmin(request) == True:
            try:
                query = CoinsModel.objects.get(id=id)
                return render(request,'adminsection/update-coin.html',{"Coin":query})
            except:
                messages.info(request, "Something went wrong!")
                return redirect('AdminAllCoins')
        else:
            return render(request,'404.html')


    def post(self,request,id):
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
        promotedCoin = request.POST['promoted_coin']
        # pushing record to the db
        query = CoinsModel.objects.filter(id=id).update(User_id=request.user.id, token_name=coinName, token_symbol=coinSymbol,
                           token_description=coinDesc, is_coin_launched=isCoinLaunched,
                           launch_date=lauchDate, token_logo_link=tokenLogoLink, presale=coinPresale,
                           smart_chain_address=smartContract,
                           ethereum_address=ethereumContract, other_links=otherLinks, website=website,
                           telegram=telegram, twitter=twitter, reddit=redit, is_promoted_coin=promotedCoin)
        if query:
            messages.info(request, "A coin was updated successfully!")
            return redirect('AdminAllCoins')
        else:
            messages.info(request, "Something went wrong!")
            return redirect('AdminAllCoins')




'''
#############################
Admin votes related stuff 
#############################
'''
# Admin all votes view
@login_required(login_url="AdminLogin")
def adminAllVotesView(request):
    if checkAdmin(request) == True:
        query = VotesModel.objects.all().order_by('-id')
        paginator = Paginator(query, 15)
        page = request.GET.get('page')
        query = paginator.get_page(page)
        return render(request,'adminsection/votes.html',{"Data":query})
    else:
        return render(request,'404.html')



# Admin view for rejecting vote
@login_required(login_url="AdminLogin")
def rejectVote(request,id):
    if checkAdmin(request) == True:
        try:
            query = VotesModel.objects.get(id=id)
            query.vote_status = "Rejected"
            query.save()
            messages.info(request, f"Vote was rejected successfully.")
            return redirect('AdminAllVotes')
        except:
            messages.info(request,"Something went wrong!")
            return redirect('AdminAllVotes')
    else:
        return render(request,'404.html')



# Admin view for deleting vote
@login_required(login_url="AdminLogin")
def deleteVote(request,id):
    if checkAdmin(request) == True:
        try:
            query = VotesModel.objects.get(id=id)
            query.delete()
            messages.info(request, f"Vote was deleted successfully.")
            return redirect('AdminAllVotes')
        except:
            messages.info(request,"Something went wrong!")
            return redirect('AdminAllVotes')
    else:
        return render(request,'404.html')




'''
#############################
Admin users related stuff 
#############################
'''
# Admin users view
@login_required(login_url="AdminLogin")
def adminAllUsersView(request):
    if checkAdmin(request) == True:
        query = Accounts.objects.all().order_by('-id')
        paginator = Paginator(query, 15)
        page = request.GET.get('page')
        query = paginator.get_page(page)
        return render(request,'adminsection/users.html',{"Data":query})
    else:
        return render(request,'404.html')



# Add Admin view.
class AddAdminView(View):
    def get(self, request):
        if checkAdmin(request) == True:
            return render(request,'adminsection/add-admin.html')
        else:
            return render(request,'404.html')


    def post(self, request):
        fullname = request.POST['fullname']
        email = request.POST['email']
        password = request.POST['password']

        if Accounts.objects.filter(email=email).exists():
            messages.info(request, f'Sorry an account is already created on {email}. Please use another one.')
            return render(request, 'adminsection/add-admin.html')
        else:
            # Creating user account
            user = Accounts.objects.create_superuser(fullname=fullname, email=email, password=password, username=fullname)
            user.save()
            messages.info(request,'A new admin was added successfully!')
            return redirect('AdminAllUsers')



# Admin deleting user
@login_required(login_url="AdminLogin")
def deleteUser(request,id):
    if checkAdmin(request) == True:
        try:
            query = Accounts.objects.get(id=id)
            query.delete()
            messages.info(request, f"User was deleted successfully.")
            return redirect('AdminAllUsers')
        except:
            messages.info(request,"Something went wrong!")
            return redirect('AdminAllUsers')
    else:
        return render(request,'404.html')



# Admin user update view.
class UpdateUserAdminView(View):
    def get(self, request,id):
        try:
            if checkAdmin(request) == True:
                query = Accounts.objects.get(id=id)
                return render(request, 'adminsection/update-user.html',{"User":query})
            else:
                return render(request, '404.html')
        except:
            messages.info(request,"Something went wrong!")
            return redirect('AdminAllUsers')


    def post(self, request,id):
        fullname = request.POST['fullname']
        email = request.POST['email']

        try:
            query = Accounts.objects.get(id=id)
            if query.email == email:
                # updating user
                query.fullname = fullname
                query.save()
                messages.info(request, 'The account was updated successfully!')
                return redirect('AdminAllUsers')
            elif Accounts.objects.filter(email=email).exists():
                messages.info(request, f'Sorry an acccout is already created on {email}. Please use another one!')
                return redirect('UpdateUserAdmin',id)
            else:
                # updating user with new email
                query.fullname = fullname
                query.email = email
                query.save()
                messages.info(request, 'The account was updated successfully!')
                return redirect('AdminAllUsers')
        except:
            messages.info(request,"Something went wrong!")
            return redirect('AdminAllUsers')
