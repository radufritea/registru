from django.contrib import admin
from .models import Category, PriceEntry, Product, Zone, County, Agent, Channel, Client, Shop, ShopType, Visit, WeekPlan, ProductInfo, Brand, Producer, PriceEntry

# Register your models here.
admin.site.register(Category)
admin.site.register(Channel)
admin.site.register(ShopType)
admin.site.register(Visit)
admin.site.register(Brand)
admin.site.register(Producer)
admin.site.register(PriceEntry)

# REMEMBER: The order and view of Models are in settings.py ADMIN_REORDER

@admin.register(WeekPlan)
class WeekPlanAdmin(admin.ModelAdmin):
	list_display = ('agent', 'start_date', 'end_date')
	ordering = ('agent', 'start_date',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'weight', 'unit', 'category', 'packing')
	ordering = ('category', 'name',)
	search_fields = ('name',)

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
	list_display = ('user', 'zone')
	ordering = ('zone', 'user',)

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
	list_display = ('name', 'area',)
	ordering = ('name',)

@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
	list_display = ('name', 'zone', 'area',)
	ordering = ('name',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
	list_display = ('loc_name', 'zone', 'county', 'city', 'channel', 'distributor')
	ordering = ('name', 'zone', 'county', 'channel')
	search_fields = ('name', )

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
	list_display = ('name', 'client', 'county', 'city')
	ordering = ('name', 'client', 'county',)
	search_fields = ('name', 'client',)

@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
	list_display = ('name', 'weight', 'unit', 'category', 'packing', 'brand', 'producer')
	ordering = ('name', 'brand', 'producer',)
	search_fields = ('name', 'brand', 'producer',)

# @admin.register(PriceEntry)
# class PriceEntryAdmin(admin.ModelAdmin):
# 	list_display = ('product', 'price_value')
# 	ordering = ('product', 'price_value',)
# 	search_fields = ('product',)