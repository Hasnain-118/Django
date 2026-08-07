import datetime

from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from home.models import Contact

# Create your views here.

def index(request):
    context = {
        'variable1': "Hasnain is great",
        'variable2': "Ahmer is great",
    }
    return render(request, 'index.html', context)
    # return HttpResponse("Hello World! This is my first Django project.")
def about(request):
    # return HttpResponse("This is the about page of my first Django project.")
    return render(request, 'about.html')
def services(request):
    # return HttpResponse("This is the services page of my first Django project.")
    return render(request, 'services.html')
def contact(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name , email=email, phone=phone, desc=desc, date=datetime.today())
        contact.save()
        # success message after submitting the contact form
        from django.contrib import messages
        messages.success(request, 'Your form submitted successfully!')
    # return HttpResponse("This is the contact page of my first Django project.")
    return render(request, 'contact.html')