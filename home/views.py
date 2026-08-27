from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime

from .models import Contact, Book
from .forms import SignUpForm, BookForm

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages


from django.core.paginator import Paginator
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# =========================================================
# HOME
# =========================================================
def index(request):

    books = Book.objects.all().order_by('-id')

    paginator = Paginator(books, 20)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    latest_books = Book.objects.order_by('-id')[:3]

    return render(
        request,
        'index.html',
        {
            'books': page_obj,
            'page_obj': page_obj,
            'latest_books': latest_books,
            'total_books': paginator.count,
        }
    )


# =========================================================
# SEARCH  BOOKS
# =========================================================

def search_books(request):
    query = request.GET.get('q', '').strip()

    books = Book.objects.none()

    if query:
        books = Book.objects.filter(
            title__icontains=query
        ) | Book.objects.filter(
            author__icontains=query
        ) | Book.objects.filter(
            quote__icontains=query
        )

    context = {
        'query': query,
        'books': books,
    }

    return render(request, 'search_results.html', context)

# =========================================================
# BASIC PAGES
# =========================================================

def about(request):
    return render(request, 'about.html')


def services(request):
    return redirect('about')


def contact(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone','')
        description = request.POST.get('desc','')

        contact = Contact(
            name=name,
            email=email,
            phone=phone,
            description=description,
            date=datetime.today()
        )

        contact.save()

        messages.success(
            request,
            'Your form submitted successfully!'
        )

    return render(request, 'contact.html')


# =========================================================
# SIGN UP
# =========================================================

def signup_view(request):

    if request.method == 'POST':

        form = SignUpForm(request.POST)

        if form.is_valid():

            user = form.save()

            # Automatically login after signup
            login(request, user)

            messages.success(
                request,
                'Account created successfully!'
            )

            return redirect('home')

        else:

            messages.error(
                request,
                'Please correct the errors below.'
            )

    else:

        form = SignUpForm()

    return render(
        request,
        'signup.html',
        {'form': form}
    )


# =========================================================
# SIGN IN
# =========================================================

def signin_view(request):

    if request.method == 'POST':

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(
                username=username,
                password=password
            )

            if user is not None:

                login(request, user)

                messages.success(
                    request,
                    f'Welcome back, {username}!'
                )

                # Redirect to the page user originally requested
                next_url = (
                    request.POST.get('next')
                    or request.GET.get('next')
                )

                if next_url:
                    return redirect(next_url)

                return redirect('home')

        else:

            messages.error(
                request,
                'Invalid username or password.'
            )

    else:

        form = AuthenticationForm()

    return render(
        request,
        'signin.html',
        {'form': form}
    )


# =========================================================
# SIGN OUT
# =========================================================

def signout_view(request):

    logout(request)

    messages.success(
        request,
        'You have been logged out.'
    )

    return redirect('home')


# =========================================================
# READ BOOK
# =========================================================

@login_required
def read_book(request, book_id):

    book = get_object_or_404(
        Book,
        id=book_id
    )

    return render(
        request,
        'read.html',
        {'book': book}
    )


# =========================================================
# ADMIN / STAFF CHECK
# =========================================================

def is_admin(user):
    return user.is_staff


# =========================================================
# ADD BOOK
# =========================================================

@login_required
@user_passes_test(is_admin)
def add_book(request):

    if request.method == 'POST':

        form = BookForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Book added successfully!'
            )

            return redirect('home')

        else:

            messages.error(
                request,
                'Please correct the errors below.'
            )

    else:

        form = BookForm()

    return render(
        request,
        'add_book.html',
        {'form': form}
    )


# =========================================================
# MANAGE BOOKS
# =========================================================

@login_required
@user_passes_test(is_admin)

def manage_books(request):

    query = request.GET.get('q', '').strip()

    books = Book.objects.all().order_by('-id')

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query)
        )

    paginator = Paginator(books, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'manage_books.html',
        {
            'books': page_obj,
            'page_obj': page_obj,
            'query': query,
        }
    )

# =========================================================
# DELETE BOOK
# =========================================================

@login_required
@user_passes_test(is_admin)
def delete_book(request, book_id):

    book = get_object_or_404(
        Book,
        id=book_id
    )

    book_title = book.title

    book.delete()

    messages.success(
        request,
        f'"{book_title}" deleted successfully!'
    )

    return redirect('manage_books')
# =========================================================
# Edit BOOK
# =========================================================


@login_required
@user_passes_test(is_admin)
def edit_book(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':

        form = BookForm(
            request.POST,
            request.FILES,
            instance=book
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Book updated successfully!'
            )

            return redirect('manage_books')

    else:

        form = BookForm(instance=book)

    return render(
        request,
        'edit_book.html',
        {'form': form, 'book': book}
    )





# =========================================================
# CATEGORY BOOKS
# =========================================================
def category_books(request, category_slug):
    books = Book.objects.filter(
        category=category_slug
    ).order_by('-id')

    category_display = dict(
        Book.CATEGORY_CHOICES
    ).get(category_slug, category_slug)

    context = {
        'books': books,
        'category_display': category_display,
    }

    return render(
        request,
        'category_books.html',
        context
    )


@login_required
def mark_notifications_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect(request.GET.get('next', 'home'))