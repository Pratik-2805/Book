from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, Books, Review
from .serializers import UserSerializer, LoginSerializer, BookSerializer, ReviewSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ReviewForm, BookForm
from django.db.models import Count
import random
from django.core.paginator import Paginator


def home(request):
    all_books = list(Books.objects.all())
    featured_books = random.sample(all_books, min(4, len(all_books))) if all_books else []
    return render(request, 'books/home.html', {'featured_books': featured_books})

def book_list(request):
    books = Books.objects.all()
    search = request.GET.get('search', '').strip()
    author = request.GET.get('author', '')
    genre = request.GET.get('genre', '')
    if search:
        books = books.filter(
            title__icontains=search
        ) | books.filter(
            author__icontains=search
        ) | books.filter(
            genres__icontains=search
        )
    if author:
        books = books.filter(author__icontains=author)
    if genre:
        books = books.filter(genres__icontains=genre)

    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST' and request.user.is_authenticated:
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.created_by = request.user
            book.save()
            messages.success(request, f'Book "{book.title}" added successfully!')
            return redirect('book_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm() if request.user.is_authenticated else None

    return render(request, 'books/book_list.html', {
        'books': page_obj,
        'form': form,
        'page_obj': page_obj,
        'author': author,
        'genre': genre,
        'search': search,
    })

def review_detail(request, pk):
    book = get_object_or_404(Books, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect('review_detail', pk=book.pk)
    else:
        form = ReviewForm()
    return render(request, 'books/review_detail.html', {
        'book': book,
        'form': form,
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('book_list')  # Change 'home' to your home page name
        else:
            return render(request, 'books/login.html', {'error': 'Invalid credentials'})
    return render(request, 'books/login.html')

def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'books/register.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('login')
    return render(request, 'books/register.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def about(request):
    return render(request, 'books/about.html')

def contact(request):
    return render(request, 'books/contact.html')