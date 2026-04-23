from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView
import json, random, time, urllib.request

from .models import ItemList

def searchFunction(request):
    #    search_list = {}
    if request.method == "POST":
        search = request.POST.get(
            "search_item", None
        )  # Allows user to enter search parameters
        searchUrl = (
            f"https://steamcommunity.com/market/search/render/?query={search}&start=0"
            f"&count=10&search_descriptions=0&sort_column=default&sort_dir=desc&norender=1"
        )

        r = urllib.request.urlopen(searchUrl)  # Get page

        getTotalItems = r.read().decode('utf-8')  # get page content
        getTotalItems = json.loads(getTotalItems)  # convert to JSON

        totalItems = getTotalItems["total_count"]  # get total count
        search_list = {}
        
        for currPos in range(0, totalItems + 50, 50):
            time.sleep(random.uniform(0.5, 2.5))

            itemsUrl = (
                f"https://steamcommunity.com/market/search/render/?query={search}&start={currPos}"
                f"&count=100&search_descriptions=0&sort_column=default&sort_dir=desc&norender=1&count=5000"
            )
            getAllItems = urllib.request.urlopen(itemsUrl)
            Searchtext = "Search results for: {search}"
            #                ('Items ' + str(currPos) + ' out of ' + str(totalItems) + ' code: ' + str(getAllItems.status_code))

            allItems = getAllItems.read().decode('utf-8')
            allItems = json.loads(allItems)
            allItems = allItems["results"]
            
        for currItem in allItems:
            if currItem["asset_description"]["tradable"]:
                item_data = ItemList(
                    gameID=currItem["asset_description"]["appid"],
                    gameName=currItem["app_name"],
                    itemName=currItem["name"],
                    currentPrice=currItem["sell_price_text"],
                )
                item_data.save()
                search_list = ItemList.objects.all().order_by("-id")
            #   table = ItemTable(ItemList.objects.all()) {'table': table}

        return render(
            request,
            "search_results.html",
            {"search_list": search_list, "Search Text": Searchtext},
        )
    #        allItemNames = list(set(allItemNames))  # to make sure there aren't duplicates
    else:
        Searchtext = "Could not find Tradable Item"
        return render(
            request, 
            "search_results.html",
            {"search_list": [], "Search Text": Searchtext}
        )


# Create your views here.
class HomePageView(TemplateView):
    template_name = "index.html"


class SearchResultsView(TemplateView):
    def post(self, request, *args, **kwargs):
        return searchFunction(request)


class ItemDetailsView(TemplateView):
    template_name = "item_details.html"


class ErrorPage(TemplateView):
    template_name = "404.html"


