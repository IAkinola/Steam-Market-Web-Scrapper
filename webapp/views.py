from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core.serializers import serialize
import json, random, time, urllib.request

from .models import ItemList


def searchFunction(request):
    Searchtext = ""

    if request.method == "POST":
        search = request.POST.get(
            "search_item", None
        )  # Allows user to enter search parameters
        all_items = []
        searchUrl = (
            f"https://steamcommunity.com/market/search/render/?query={search}&start=0"
            f"&count=10&search_descriptions=0&sort_column=default&sort_dir=desc&norender=1"
        )

        r = urllib.request.urlopen(searchUrl)  # Get page
        getTotalItems = r.read().decode("utf-8")  # get page content
        getTotalItems = json.loads(getTotalItems)  # convert to JSON
        totalItems = getTotalItems["total_count"]  # get total count

        Searchtext = search

        for currPos in range(0, totalItems + 50, 50):
            time.sleep(random.uniform(0.5, 2.5))

            itemsUrl = (
                f"https://steamcommunity.com/market/search/render/?query={search}&start={currPos}"
                f"&count=100&search_descriptions=0&sort_column=default&sort_dir=desc&norender=1&count=5000"
            )
            getAllItems = urllib.request.urlopen(itemsUrl)
            allItems = getAllItems.read().decode("utf-8")
            allItems = json.loads(allItems)
            allItems = allItems["results"]

            # Process items inside the pagination loop
            # Takes only tradable items
            for currItem in allItems:
                if currItem["asset_description"]["tradable"]:
                    item_data = {
                        "gameID": currItem["asset_description"]["appid"],
                        "gameName": currItem["app_name"],
                        "itemName": currItem["name"],
                        "currentPrice": currItem["sell_price"],
                        "itemUrl": "https://community.fastly.steamstatic.com/economy/image/"
                        + currItem["asset_description"]["icon_url"],
                    }
                    all_items.append(item_data)

        request.session["search_items"] = all_items
        request.session["search_term"] = search

    else:
        # Retrieve items from session
        all_items = request.session.get("search_items", [])
        search_term = request.session.get("search_term", "")
        Searchtext = search_term

    # Pagination
    pagination = Paginator(all_items, 10)  # Show 10 items per page
    page_number = request.GET.get("page")
    page_obj = pagination.get_page(page_number)

    return render(
        request,
        "search_results.html",
        {"search_list": page_obj, "Search Text": Searchtext},
    )


def detailsPage(request, item_name):
    # Get all items from session
    all_items = request.session.get("search_items", [])

    # Finding the selected item
    selected_item = None
    for item in all_items:
        if item["itemName"] == item_name:
            selected_item = item
            break

    if selected_item:
        # Store in different session object
        request.session["selectedItemName"] = selected_item["itemName"]
        request.session["selectedImgLink"] = selected_item["itemUrl"]
        request.session["selectedCurrentPrice"] = selected_item["currentPrice"]

    print(selected_item)
    return render(request, 'item_details.html')


# Create your views here.
class HomePageView(TemplateView):
    template_name = "index.html"


class SearchResultsView(TemplateView):
    template_name = "search_results.html"

    def post(self, request, *args, **kwargs):
        return searchFunction(request)

    def get(self, request, *args, **kwargs):
        return searchFunction(request)


class ItemDetailsView(TemplateView):
    template_name = "item_details.html"

    def get(self, request, item_name, *args, **kwargs):
        return detailsPage(request, item_name)


class ErrorPage(TemplateView):
    template_name = "404.html"
