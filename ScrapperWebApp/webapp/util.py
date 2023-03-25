import requests
import json
import random
import time


# Search for item
def searchfunction(item):
    searchUrl = f"https://steamcommunity.com/market/search/render/?query={item}&start=0" \
                f"&count=100&search_descriptions=0&sort_column=default&sort_dir=desc&norender=1"

    # Get page
    r = requests.get(searchUrl)
    r = r.content
    formattedResult(r)


# turn content to a json format
def makeJsonfile(pageContent):
    jsonfile = json.loads(pageContent)
    return jsonfile


# Formatting results to return a dictionary
def formattedResult(page):
    resultDictionary = {}

    # Get total number of items 
    pageContent = makeJsonfile(page)
    totalItems = pageContent['total_count']
    item = pageContent['searchdata']['query']

    # Scrap through data
    for currPos in range(0, totalItems + 50, 50):
        time.sleep(random.uniform(0.5, 2.5))

        itemsUrl = f"https://steamcommunity.com/market/search/render/?query={item}&start={currPos}" \
                   f"&count=100&search_descriptions=0&sort_column=default&sort_dir=desc&norender=1"

        getAllItems = requests.get(itemsUrl)
        allItems = getAllItems.content
        allItems = makeJsonfile(allItems)
        
        itemResults = allItems['results']

        tradable = itemResults[currPos]['asset_description']['tradable']

        if tradable == 1:
                itemName = itemResults[currPos]['name']
                resultDictionary[itemName] = {
                    "Game Name": itemResults[currPos]['app_name'],
                    "Game ID": itemResults[currPos]['asset_description']['appid'],
                    "Sell Price": itemResults[currPos]['sell_price_text']
                }
    print(resultDictionary)

    # for totalitems, loop through page, call page again? to loop through the url giving using variables from current function
#        itemsUrl = f"https://steamcommunity.com/market/search/render/?query={item}&start={currPos}" \
#                   f"&count=100&search_descriptions=0&sort_column=default&sort_dir=desc&norender=1&count=5000"

#       getAllItems = requests.get(itemsUrl)

        # Change to json format
#       allItems = makeJsonfile(getAllItems)
#       allItems = allItems['results']

        # Append into dictionary
  #      for currItem in allItems:
   #         if currItem['asset_description']['tradable']:
    #            itemName = currItem['name']
     #           resultDictionary[itemName] = {
      #              "Game Name": currItem['app_name'],
       #             "Game ID": currItem['asset_description']['appid'],
        #            "Sell Price": currItem['sell_price_text']
#                }
#    return resultDictionary

#  dataUrl = f"https://steamcommunity.com/market/listings/{idNumber}/{currItemHTTP}"
# for item in allItemNames:
#    for idNumber in gameID:
#        currItemHTTP = item.replace(' ', '%20')
#        currItemHTTP = currItemHTTP.replace('&', '%26')
#
#        dataUrl = f"https://steamcommunity.com/market/listings/{idNumber}/{currItemHTTP}"
#        itemLinks.append(dataUrl)

#       itemList = requests.get(dataUrl)

# Some app names = "Steam"

# For testing
while True:
    search = input("Search for: ")
    if search == "exit":
        break
    searchfunction(search)

    