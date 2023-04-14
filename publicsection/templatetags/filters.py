from django import template
from adminsection.models import *
from adminsection.other_logics import *
register = template.Library()


# filter for total votes
@register.filter(name='totalVotes')
def totalVotes(coinId):
    total = VotesModel.objects.filter(Coin_id=coinId,vote_status="Approved").count()
    return total


# filter for getting the checking the user vote through ip and register
@register.filter(name='checkUserVoteF')
def checkUserVote(request,coinId):
    # checking coin vote for user
    ip = GetIp(request)
    ipQuery = VotesModel.objects.filter(Coin_id=coinId,user_ip=ip).exists()
    userQuery = VotesModel.objects.filter(Coin_id=coinId,user_id=checkLoginUserVote(request)).exists()

    if ipQuery or userQuery:
        return True
    else:
        return False
