from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('book_list/', book_list, name='book_list'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('review/<int:pk>/', views.review_detail, name='review_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    # path('api/', include('books.api_urls')),
]