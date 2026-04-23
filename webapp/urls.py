from django.urls import path

from .views import HomePageView, SearchResultsView, ItemDetailsView, ErrorPage

urlpatterns = [
    path("", HomePageView.as_view(), name='index'),
    path("search/", SearchResultsView.as_view(), name="search_results"),
    path("search/itemName", ItemDetailsView.as_view(), name="item_details"),
    path("404", ErrorPage.as_view(), name="404"),
]