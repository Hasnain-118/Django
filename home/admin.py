from django.contrib import admin
from home.models import Contact
from home.views import contact
# Register your models here.
admin.site.register(Contact)

from .models import Book, Contact

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'rating')
    search_fields = ('title', 'author')