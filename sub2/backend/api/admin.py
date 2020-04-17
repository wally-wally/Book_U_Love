from django.contrib import admin
from .models import Category, Book, Review

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'id', 'name',)


class BookAdmin(admin.ModelAdmin):
    list_display = ('pk', 'isbn', 'title', 'description', 'category', 'publisher')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'content', 'score', 'book', 'user')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Review, ReviewAdmin)
