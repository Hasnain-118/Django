from .models import Book


def category_choices(request):
    return {
        'category_choices': Book.CATEGORY_CHOICES
    }