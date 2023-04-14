from .models import *
from usersection.models import Accounts

def adminTotals(request):
    totalVotes = VotesModel.objects.all().count()
    totalUsers = Accounts.objects.all().count()
    totalImpressions = ImpressionsModel.objects.all().count()
    totalCoins = CoinsModel.objects.all().count()

    return {"TotalVotes":totalVotes,"TotalUsers":totalUsers,"TotalImpressions":totalImpressions,
            "TotalCoins":totalCoins}

