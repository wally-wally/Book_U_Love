from django.contrib import admin
from .models import Book, Review, DetailCategory

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('pk', 'isbn', 'title', 'description', 'publisher')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'content', 'score', 'book', 'user')


admin.site.register(Book, BookAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(DetailCategory)
