from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('posted-coins/',postedCoins,name="UserPostedCoins"),
    path('declined-coins/',unlistedCoins,name="UserUnlistedCoins"),
    path('pending-coins/',pendingCoins,name="UserPendingCoins"),
    path('user-dashboard/',userDashboard,name="UserDashboard"),
    path('user-logout/',logoutView,name="LogoutView"),
    path('add-coin/',login_required(UserAddCoin.as_view()),name="UserAddCoinView"),
    path('update-profile/',login_required(UserUpdateProfile.as_view()),name="UserUpdateProfileView"),


    # Setting and customizing default views of Password change and forgot
    path('reset_password/',
    auth_views.PasswordResetView.as_view(template_name="password-reset-templates/reset_password.html"),
    name="reset_password"),

    path('reset_password_sent/',
    auth_views.PasswordResetDoneView.as_view(template_name="password-reset-templates/reset_password_sent.html"),
    name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name="password-reset-templates/reset_password_form.html"),
    name="password_reset_confirm"),

    path('password_reset_complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name="password-reset-templates/reset_password_completed.html"),
    name="password_reset_complete"),

    path('password_change/',
    auth_views.PasswordChangeView.as_view(template_name="password-reset-templates/password_change.html"),
    name="password_change"),


    path('password_change_done/',
    auth_views.PasswordChangeDoneView.as_view(template_name="password-reset-templates/password_changed.html"),
    name="password_change_done"),

]
