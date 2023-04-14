from django.urls import path
from .views import *

urlpatterns = [
    path('login/',LoginView.as_view(),name="LoginView"),
    path('signup/',SignupView.as_view(),name="SignupView"),
    path('',indexView,name="IndexView"),
    path('shill-coin/',shillView,name="ShillView"),
    path('promotion-coin/',promoteView,name="PromoteView"),
    path('newsletter/',NewsletterView.as_view(),name="NewsletterView"),
    path('coin/<slug:slug>/',coinDetails,name="CoinDetails"),
    path('impression-submit/<slug:slug>/',submitImpression,name="ImpressionSubmit"),
    path('submit-vote-user/<int:id>/',submitVote,name="SubmitVoteUser"),
]
