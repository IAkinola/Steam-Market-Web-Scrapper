import requests
import json
import random
import time

# Search for item
def searchfunction(item):
    searchUrl = f"https://steamcommunity.com/market/search/render/?query={item}&start=0" \
                f"&count=10&search_descriptions=0&sort_column=default&sort_dir=desc&norender=1"

    # Get page
    r = requests.get(searchUrl) 
    return r


# turn content to a json format
def makeJsonfile(pageContent):
    
    jsonfile = pageContent.content
    jsonfile = json.loads(jsonfile)
    
    return jsonfile


# Formating results to return a dictiuonary
def formattedResult(item):

    resultDictionary = {}
    
    # Get total number of items 
    gettotalItems = searchfunction(item)
    totalItems = makeJsonfile(gettotalItems)
    totalItems = gettotalItems['total_count']

    # Scrap through data
    for currPos in range(0, totalItems + 50, 50):
        time.sleep(random.uniform(0.5, 2.5))

        itemsUrl = f"https://steamcommunity.com/market/search/render/?query={item}&start={currPos}" \
                   f"&count=100&search_descriptions=0&sort_column=default&sort_dir=desc&norender=1&count=5000"
        
        getAllItems = requests.get(itemsUrl)

        # Change to json format
        allItems = makeJsonfile(getAllItems)
        allItems = allItems['results']

        # Append into dictionary
        for currItem in allItems:
            if currItem['asset_description']['tradable']:
                itemName = currItem['name']
                resultDictionary[itemName] = {
                    "Game Name": currItem['app_name'],
                    "Game ID": currItem['asset_description']['appid'],
                    "Sell Price": currItem['sell_price_text']
                }
    return resultDictionary