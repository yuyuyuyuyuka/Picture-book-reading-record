from django.contrib import admin
from .models import Child, Book

class ChildAdmin(admin.ModelAdmin):
    list_display = ('name', 'birthday', 'family_id', 'created_at', 'update_at')
    search_fields = ['name']
    
admin.site.register(Child, ChildAdmin)


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publisher', 'cover_image', 'created_at', 'update_at')
    search_fields = ['title']
    
admin.site.register(Book, BookAdmin)