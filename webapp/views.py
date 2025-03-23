from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView, ListView
from django_tables2 import SingleTableView

import json, random, time

from .models import ItemList
from .tables import ItemTable

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'index.html'

class SearchResultsView(SingleTableView):
    model = ItemList
    table_class =   ItemTable
    template_name = 'search_results.html'

    def searchFunction(request):
    #    search_list = {}
        if request.method == 'POST':
            search = request.POST.get('searchbar', None)  # Allows user to enter search parameters
            searchUrl = f"https://steamcommunity.com/market/search/render/?query={search}&start=0" \
                        f"&count=10&search_descriptions=0&sort_column=default&sort_dir=desc&norender=1"

            r = request.get(searchUrl)  # Get page

            getTotalItems = r.content  # get page content
            getTotalItems = json.loads(getTotalItems)  # convert to JSON

            totalItems = getTotalItems['total_count']  # get total count

            for currPos in range(0, totalItems + 50, 50):
                time.sleep(random.uniform(0.5, 2.5))

                itemsUrl = f"https://steamcommunity.com/market/search/render/?query={search}&start={currPos}" \
                           f"&count=100&search_descriptions=0&sort_column=default&sort_dir=desc&norender=1&count=5000"
                getAllItems = request.get(itemsUrl)
                Searchtext = "Search results for: {search}"
#                ('Items ' + str(currPos) + ' out of ' + str(totalItems) + ' code: ' + str(getAllItems.status_code))

                allItems = getAllItems.content
                allItems = json.loads(allItems)
                allItems = allItems['results']

            for currItem in allItems:
                if currItem['asset_description']['tradable']:
                    item_data = ItemList(
                        gameID = currItem['asset_description']['appid'],
                        gameName = currItem['app_name'],
                        itemName = currItem['name'],
                        currentPrice = currItem['sell_price_text']
                    )
                    item_data.save()
                    search_list = ItemList.all().order_by('-id')
                #   table = ItemTable(ItemList.objects.all()) {'table': table}

            return render(request, Searchtext, {'search_list': search_list})
#        allItemNames = list(set(allItemNames))  # to make sure there aren't duplicates
        else:
            Searchtext = "Could not find Tradable Item"
            return(Searchtext)
    