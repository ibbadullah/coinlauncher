from django.db import models
from encrypted_fields.fields import SearchField, EncryptedCharField
from django.utils import timezone
import math
from django.template.defaultfilters import slugify

# Coins model.
class CoinsModel(models.Model):
    User = models.ForeignKey("usersection.Accounts",verbose_name="userCoin",on_delete=models.CASCADE)
    token_name = models.CharField(max_length=200,null=True,blank=True)
    token_symbol = models.CharField(max_length=200, null=True, blank=True)
    token_description = models.TextField(max_length=2000, null=True, blank=True)
    presale = models.CharField(max_length=50, null=True, blank=True,default="No")
    token_logo_link = models.CharField(max_length=2000, null=True, blank=True)
    launch_date = models.DateTimeField(null=True,blank=True)
    is_coin_launched = models.CharField(max_length=50, null=True, blank=True,default="Yes")
    smart_chain_address = models.TextField(max_length=1000, null=True, blank=True)
    ethereum_address = models.TextField(max_length=1000, null=True, blank=True)
    other_links = models.TextField(max_length=2000, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    telegram = models.CharField(max_length=1000, null=True, blank=True)
    twitter = models.CharField(max_length=1000, null=True, blank=True)
    reddit = models.CharField(max_length=1000, null=True, blank=True)
    coin_status = models.CharField(max_length=100, null=True, blank=True,default="Listed")
    is_promoted_coin = models.CharField(max_length=10,null=True,blank=True,default="No")
    added_time = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    coin_slug = models.SlugField(max_length=255,unique=True,null=True,blank=True)


    # Unique slug generating for coin
    def generateSlug(self):
        if not self.id and not self.coin_slug:
            slug = slugify(self.token_name)
            slug_exists = True
            counter = 1
            self.coin_slug = slug
            while slug_exists:
                try:
                    slug_exits = CoinsModel.objects.get(coin_slug=slug)
                    if slug_exits:
                        slug = self.coin_slug + '-' + str(counter)
                        counter += 1
                except CoinsModel.DoesNotExist:
                    self.coin_slug = slug
                    break


    # function for timestamp
    def timeStamp(self):
        now = timezone.now()
        diff = now - self.launch_date
        # First finding checking for seconds
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds
            if seconds == 1:
                return str(seconds) + " second ago"
            else:
                return str(seconds) + " seconds ago"

        # Checking for minutes
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)
            if minutes == 1:
                return str(minutes) + " minute ago"
            else:
                return str(minutes) + " minutes ago"

        # Checking for hours
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)
            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"

        # Checking for days 1 - 30
        if diff.days >= 1 and diff.days < 30:
            days = diff.days
            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"

        # Checking for months 1 - 11
        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days / 30)
            if months == 1:
                return str(months) + " month ago"
            else:
                return str(months) + " months ago"

        # Now checking for years
        if diff.days >= 365:
            years = math.floor(diff.days / 365)
            if years == 1:
                return str(years) + " year ago"
            else:
                return str(years) + " years ago"


    # Overriding save method
    def save(self,*args,**kwargs):
        self.generateSlug()
        super(CoinsModel, self).save(*args,**kwargs)

    class Meta:
        db_table = "coins_model"

    def get_absolute_url(self):
        return f"coin/{self.coin_slug}/"



# votes model
class VotesModel(models.Model):
    Coin = models.ForeignKey(CoinsModel,verbose_name="coin_vote",on_delete=models.CASCADE)
    user_id = models.IntegerField(null=True,blank=True,default=0)
    user_ip = models.CharField(max_length=200,null=True,blank=True)
    vote_status = models.CharField(max_length=100,null=True,blank=True,default="Approved")
    vote_added_time = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    class Meta:
        db_table = "coin_votes_model"


# impressions model
class ImpressionsModel(models.Model):
    User = models.ForeignKey("usersection.Accounts", verbose_name="userImpression", on_delete=models.CASCADE)
    Coin = models.ForeignKey(CoinsModel,verbose_name="coin_impression",on_delete=models.CASCADE)
    impression_text = models.TextField(max_length=2000,null=True,blank=True)
    impression_added_time = models.DateTimeField(auto_now_add=True,null=True,blank=True)


    # function for timestamp
    def timeStamp(self):
        now = timezone.now()
        diff = now - self.impression_added_time
        # First finding checking for seconds
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds
            if seconds == 1:
                return str(seconds) + " second ago"
            else:
                return str(seconds) + " seconds ago"

        # Checking for minutes
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)
            if minutes == 1:
                return str(minutes) + " minute ago"
            else:
                return str(minutes) + " minutes ago"

        # Checking for hours
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)
            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"

        # Checking for days 1 - 30
        if diff.days >= 1 and diff.days < 30:
            days = diff.days
            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"

        # Checking for months 1 - 11
        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days / 30)
            if months == 1:
                return str(months) + " month ago"
            else:
                return str(months) + " months ago"

        # Now checking for years
        if diff.days >= 365:
            years = math.floor(diff.days / 365)
            if years == 1:
                return str(years) + " year ago"
            else:
                return str(years) + " years ago"

    class Meta:
        db_table = "impressions_model"


# newsletter model
class NewsLetterModel(models.Model):
    _email_data = EncryptedCharField(max_length=200)
    email = SearchField(hash_key='d2465e886a5f91ca6930c77881e0378dc81b5216b7a9758c12c760f4d53a3a3c',encrypted_field_name='_email_data')
    subscribed_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = "newsletter_model"


