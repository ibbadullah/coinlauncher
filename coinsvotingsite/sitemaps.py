from django.contrib.sitemaps import Sitemap
from adminsection.models import CoinsModel
from django.shortcuts import reverse


class StaticSiteMaps(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ["IndexView","SignupView","LoginView","PromoteView","NewsletterView","ShillView"]

    def location(self, item):
        return reverse(item)



class CoinsSiteMaps(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return CoinsModel.objects.filter(coin_status="Listed")
