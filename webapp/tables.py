import django_tables2 as tables 
from .models import ItemList

class ItemTable(tables.Table):
    class Meta:
        model = ItemList
        template_name = "search_results.html"
        fields = ("index", "itemName", "currentPrice")