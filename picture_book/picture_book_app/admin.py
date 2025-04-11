from django.contrib import admin
from .models import Child, Book, ReadingComment, ReadingRecord

class ChildAdmin(admin.ModelAdmin):
    list_display = ('name', 'birthday', 'family_id', 'created_at', 'update_at')
    search_fields = ['name']
    
admin.site.register(Child, ChildAdmin)


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publisher', 'cover_image', 'created_at', 'update_at')
    search_fields = ['title']
    
admin.site.register(Book, BookAdmin)


class ReadingCommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'created_at', 'update_at')
    search_fields = ['comment']
    
admin.site.register(ReadingComment, ReadingCommentAdmin)


class ReadingRecordAdmin(admin.ModelAdmin):
    list_display = (
        'child', 'book', 'get_reading_comments', 'date', 'read_count', 'book_status',
        'photo', 'video', 'review', 'created_at', 'update_at',
    )
    search_fields = ['child__name', 'book__title','date']
    list_filter = ['child', 'book', 'date']
    date_hierarchy = 'date'
    
    # ManyToManyField の読みやすい表示用の関数
    def get_reading_comments(self,obj):
         return ", ".join([comment.comment for comment in obj.reading_comments.all()])
    get_reading_comments.short_description = '簡単記録'

admin.site.register(ReadingRecord, ReadingRecordAdmin)