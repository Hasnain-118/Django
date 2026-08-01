from django.contrib import admin
from home.models import Contact
from home.views import contact
# Register your models here.
admin.site.register(Contact)