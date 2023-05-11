from django.contrib import admin

# Register your models here.
from products.models import ProductCategory, Product, Basket

# admin.site.register(Product)
admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('name', 'description',
              ('price', 'quantity'), 'category', 'image')
    search_fields = ['name']
    ordering = ['name']


class BasketAdmin(admin.TabularInline):
    model = Basket
    readonly_fields = ['created_timestamp']
    fields = ['product', 'quantity', 'created_timestamp']
