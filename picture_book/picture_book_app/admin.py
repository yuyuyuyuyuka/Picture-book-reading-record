from django.contrib import admin
from .models import Child

class ChildAdmin(admin.ModelAdmin):
    list_display = ('name', 'birthday', 'family_id', 'created_at', 'update_at')
    search_fields = ['name']
    
admin.site.register(Child, ChildAdmin)