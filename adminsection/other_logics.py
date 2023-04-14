from adminsection.models import *
import datetime

# Admin Check for admin class base views & functions
def checkAdmin(request):
    if request.user.is_admin == True and request.user.is_staff == True and request.user.is_superuser == True:
        return True
    else:
        return False



# Returning Ip address of the user
def GetIp(request):
    x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forward:
        ip = x_forward.split(',')[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip



# view for checking login person vote
def checkLoginUserVote(request):
    if request.user.is_authenticated:
        return request.user.id
    else:
        return 0


# previous day top performer (Note this function is currently not in used)
def yesterdayTopPerformer(request):
    try:
        # getting yesterday date
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        # defining lists for total votes and ids
        indexesList = []
        totalVotesList = []
        # now doing the trick
        coinsQuery = CoinsModel.objects.filter(coin_status='Listed')
        for c in coinsQuery:
            votesQuery = VotesModel.objects.filter(Coin_id=c.id, vote_added_time__day=yesterday.day,
                                                   vote_added_time__month=yesterday.month,
                                                   vote_added_time__year=yesterday.year,vote_status="Approved").count()
            indexesList.append(c.id)
            totalVotesList.append(votesQuery)

        # Getting high votes from the list and also getting index
        highVotes = max(totalVotesList)
        topCoinIndex = totalVotesList.index(highVotes)
        yesterTperformer = indexesList[topCoinIndex]
        ytQuery = CoinsModel.objects.get(id=yesterTperformer)
        return ytQuery
    except:
        return 0






# today best
def todayBest(request):
    try:
        # getting yesterday date
        today = datetime.date.today()
        # defining dictionary for total votes and ids
        votesDic = {}
        # now doing the trick
        coinsQuery = CoinsModel.objects.filter(coin_status='Listed')
        for c in coinsQuery:
            votesQuery = VotesModel.objects.filter(Coin_id=c.id, vote_added_time__day=today.day,
                                                   vote_added_time__month=today.month,
                                                   vote_added_time__year=today.year,vote_status="Approved").count()
            # Only getting those coins that have greater than 0 votes
            if votesQuery > 0:
                votesDic[c.id] = votesQuery
        # sorting dictionary by large value. Mean displaying big votes coins first
        topCoins = sorted(votesDic, key = votesDic.get, reverse=True)
        # Displaying all the votes by ids
        return [CoinsModel.objects.get(id=id) for id in topCoins]
    except:
        return 0




# today total best
def todayTotalBest(request):
    try:
        # getting yesterday date
        today = datetime.date.today()
        # defining dictionary for total votes and ids
        votesDic = {}
        # now doing the trick
        coinsQuery = CoinsModel.objects.filter(coin_status='Listed')
        for c in coinsQuery:
            votesQuery = VotesModel.objects.filter(Coin_id=c.id, vote_added_time__day=today.day,
                                                   vote_added_time__month=today.month,
                                                   vote_added_time__year=today.year,vote_status="Approved").count()
            # Only getting those coins that have greater than 0 votes
            if votesQuery > 0:
                votesDic[c.id] = votesQuery
        # sorting dictionary by large value. Mean displaying big votes coins first
        topCoins = sorted(votesDic, key = votesDic.get, reverse=True)
        # Displaying all the votes by ids
        q = CoinsModel.objects.filter(id__in=topCoins)
        return q
    except:
        return 0




# All time best
def allTimeBest(request):
    try:
        # getting yesterday date
        today = datetime.date.today()
        # defining dictionary for total votes and ids
        votesDic = {}
        # now doing the trick
        coinsQuery = CoinsModel.objects.filter(coin_status='Listed')
        for c in coinsQuery:
            votesQuery = VotesModel.objects.filter(Coin_id=c.id,vote_status="Approved").count()
            votesDic[c.id] = votesQuery
        # sorting dictionary by large value. Mean displaying big votes coins first
        topCoins = sorted(votesDic, key = votesDic.get, reverse=True)
        # Displaying all the votes by ids
        return [CoinsModel.objects.get(id=id) for id in topCoins]
    except:
        return 0
