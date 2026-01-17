from django.contrib import admin
from .models import Search

@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    list_display = ('query', 'keywords', 'countries', 'query_type', 'size', 'created_at', 'updated_at')
    list_filter = ('query_type', 'created_at')
    search_fields = ('query', 'keywords')
    readonly_fields = ('created_at', 'updated_at')
