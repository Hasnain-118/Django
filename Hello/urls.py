"""
URL configuration for Hello project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static

# from home import views 
# from django.contrib import admin

# Changes the text at the top of every admin page and login page
admin.site.site_header = "Hasnain Admin "

# Changes the text displayed in the browser tab title
admin.site.site_title = "Hasnain Admin Portal"

# Changes the large welcome greeting on the admin homepage
admin.site.index_title = "Welcome to the Hasnain Admin Portal"


urlpatterns = [

    # Django Admin
    path('admin/', admin.site.urls),

    # django-allauth
    path('accounts/', include('allauth.urls')),

    # Home App
    path('', include('home.urls')),

] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

 