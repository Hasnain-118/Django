from django.contrib import admin
from django.urls import path
from home import views
urlpatterns = [
    path("", views.index, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("contact/", views.contact , name="contact"),
    path("signup/", views.signup_view, name="signup"),
    path("signin/", views.signin_view, name="signin"),
    path("signout/", views.signout_view, name="signout"),
    path("read/<int:book_id>/", views.read_book, name="read_book"),
    path("add-book/", views.add_book, name="add_book"),
    path("manage-books/", views.manage_books, name="manage_books"),
    path("delete-book/<int:book_id>/", views.delete_book, name="delete_book"),
]

