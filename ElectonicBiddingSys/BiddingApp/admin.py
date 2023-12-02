from django.contrib import admin
from django.contrib import admin

# Register your models here.
from .models import Category, Item


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    # list_display = ("name", "category", "price")
    list_display = ('description', 'starting_price', 'category', 'condition', 'end_date', 'start_date')
    list_filter = ("category",)
    search_fields = ("name",)
    # list_editable = ("price",)
    list_editable = ('starting_price',)
    list_per_page = 10
    # ordering = ("name",)
    ordering = ('-end_date',)

