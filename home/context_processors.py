from .models import Book


def category_choices(request):
    return {
        'category_choices': Book.CATEGORY_CHOICES
    }
def notifications(request):
    if request.user.is_authenticated:
        notifications_qs = request.user.notifications.all()

        return {
            'notifications': notifications_qs[:10],
            'unread_count': notifications_qs.filter(is_read=False).count()
        }

    return {
        'notifications': [],
        'unread_count': 0
    }
