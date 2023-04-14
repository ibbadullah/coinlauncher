from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('admin-dashboard/',adminDashbaordView,name="AdminDashboard"),
    path('192-160-1/',AdminLoginView.as_view(),name="AdminLogin"),

    # Coins related urls
    path('all-coins',adminAllCoinsView,name="AdminAllCoins"),
    path('list-coin/<int:id>/',listCoin,name="ListCoin"),
    path('unlist-coin/<int:id>/',unlistCoin,name="UnlistCoin"),
    path('delete-coin/<int:id>/',deleteCoin,name="DeleteCoin"),
    path('update-coin/<int:id>/',login_required(CoinUpdateView.as_view()),name="UpdateCoin"),
    path('admin-add-coin/',login_required(AdminAddCoin.as_view()),name="AdminAddCoin"),

    # Users related urls
    path('all-users/',adminAllUsersView,name="AdminAllUsers"),
    path('add-admin/',login_required(AddAdminView.as_view()),name="AddAdmin"),
    path('del-user-admin/<int:id>/',deleteUser,name="DeleteAdminUser"),
    path('update-user-admin/<int:id>/',login_required(UpdateUserAdminView.as_view()),name="UpdateUserAdmin"),
    path('admin-profile-update/',login_required(AdminUpdateProfile.as_view()),name="UpdateAdminProfileView"),

    # Votes related urls
    path('all-votes', adminAllVotesView, name="AdminAllVotes"),
    path('delete-vote/<int:id>',deleteVote,name="DeleteVote"),
    path('reject-vote/<int:id>',rejectVote,name="RejectVote"),
]
