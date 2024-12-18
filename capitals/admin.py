from django.contrib import admin
from .models import Capital

# Register your models here.

@admin.register(Capital)
class CapitalAdmin(admin.ModelAdmin):
    list_display = ('capital_city', 'country', 'capital_population', 'author')
    list_filter = ('country',)
    search_fields = ('capital_city', 'country')
