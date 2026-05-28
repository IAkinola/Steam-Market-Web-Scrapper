from django.contrib import admin
from .models import ItemList

# Register your models here.
@admin.register(ItemList)
class ItemListAdmin(admin.ModelAdmin):
    list_display = ('itemName', 'gameName', 'currentPrice', 'gameID')
    search_fields = ('itemName', 'gameName')
    list_filter = ('gameName',)
    readonly_fields = ('itemUrl',)
