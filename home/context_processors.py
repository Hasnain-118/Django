from django.db.utils import OperationalError, ProgrammingError

from .models import Book


def category_choices(request):
    return {
        'category_choices': Book.CATEGORY_CHOICES
    }


def notifications(request):
    empty = {
        'notifications': [],
        'unread_count': 0
    }

    if not request.user.is_authenticated:
        return empty

    try:
        notifications_qs = request.user.notifications.all()
        return {
            'notifications': notifications_qs[:10],
            'unread_count': notifications_qs.filter(is_read=False).count()
        }
    except (OperationalError, ProgrammingError):
        return empty
