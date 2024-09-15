from mptt.admin import DraggableMPTTAdmin
from django.contrib import admin

from bot.models import *


class ProductImageTabularInline(admin.TabularInline):
    model = ProductImage
    extra = 5
    fk_name = 'product'


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'interface_lang')
    list_display_links = ('telegram_id',)


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'id', 'name_uz', 'name_ru', 'parent')
    list_display_links = ('name_uz', 'name_ru')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uz', 'name_ru', 'model', 'category', 'price', 'action', 'created')
    list_display_links = ('name_uz', 'name_ru')
    list_filter = ('category', 'action')
    search_fields = ('name_uz', 'name_ru', 'model')
    list_edit_fields = ('action',)
    inlines = [ProductImageTabularInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image')
    list_display_links = ('product',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'position')
    list_display_links = ('name',)
