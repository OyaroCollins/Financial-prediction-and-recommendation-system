# smartfinance/urls.py
# Main URL configuration

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Accounts app URLs (register, login, logout)
    path('', include('accounts.urls')),
    
    # Tracker app URLs (dashboard, transactions, etc.)
    path('', include('tracker.urls')),
]