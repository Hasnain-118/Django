from django.urls import path
from home import views

urlpatterns = [
    path("", views.index, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("contact/", views.contact, name="contact"),

    path("read/<int:book_id>/", views.read_book, name="read_book"),
    path("add-book/", views.add_book, name="add_book"),
    path("manage-books/", views.manage_books, name="manage_books"),
    path("delete-book/<int:book_id>/", views.delete_book, name="delete_book"),
    path("edit-book/<int:book_id>/", views.edit_book, name="edit_book"),
    path("category/<str:category_slug>/", views.category_books, name="category_books"),
    path("search/", views.search_books, name="search_books"),

    path(
        "notifications/read/<int:notif_id>/",
        views.mark_one_read,
        name="mark_one_read"
    ),
    
    # Saari notifications read karne ke liye (aapka existing)
    path(
        "notifications/read/",
        views.mark_notifications_read,
        name="mark_notifications_read"
    ),
    
    # Single notification delete karne ke liye
    path(
        "notifications/delete/<int:notif_id>/",
        views.clear_notification,
        name="clear_notification"
    ),
]
