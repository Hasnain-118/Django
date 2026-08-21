from .models import Book


def category_choices(request):
    return {
        'category_choices': Book.CATEGORY_CHOICES
    }
def notifications(request):
    if request.user.is_authenticated:
        qs = request.user.notifications.all()[:10]

        return {
            'notifications': qs,
            'unread_count': qs.filter(is_read=False).count()
        }

    return {
        'notifications': [],
        'unread_count': 0
    }