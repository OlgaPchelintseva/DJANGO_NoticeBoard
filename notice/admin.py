from django.contrib import admin
from .models import Notice

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'created_at')
    search_fields = ('title', )
    list_filter = ('created_at', )
    readonly_fields = ('created_at', )
