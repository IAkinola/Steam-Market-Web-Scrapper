from django.shortcuts import render
from django.shortcuts import redirect
from . import util

# Create your views here.
def index(request):
    if request.method == 'POST':

        #Get form data
        form_data = request.POST
        searchName = form_data['item_name']

        if searchName.is_valid():

            # Process the form data
            util.searchfunction(searchName)
            return redirect('searchResult?result=%s' % searchName)
    else:
        return render(request, "index.html")

def searchResult(request):
    
    # Get variable from url
    result = request.GET.get('result')

    # Processing data
    resultDict = util.formattedResult(result)

    return render(request, "results.html", {'resultDict': resultDict})