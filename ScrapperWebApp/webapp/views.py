from django.shortcuts import render
from . import util

# Create your views here.
def index(request):
    return render(request, "index.html")

def searchResult(request):
    return render(request, "results.html")