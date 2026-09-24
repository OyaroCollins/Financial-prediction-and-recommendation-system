# tracker/urls.py
# This file maps URLs to view functions for the tracker app

from django.urls import path          # Django's URL routing function
from . import views                   # Import views from current folder

# urlpatterns defines all URL patterns for this app
urlpatterns = [

    #Home page
    path('', views.home, name='home'),
    
    # Dashboard - main page after login
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Transactions
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('edit/<int:transaction_id>/', views.edit_transaction, name='edit_transaction'),
    path('delete/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
    
    # Categories
    path('categories/', views.categories, name='categories'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    
    # Predictions and Recommendations
    path('predictions/', views.predictions, name='predictions'),
    path('recommendations/', views.recommendations, name='recommendations'),
    
    # Budgets
    path('budgets/', views.budgets, name='budgets'),
    path('budgets/delete/<int:budget_id>/', views.delete_budget, name='delete_budget'),

    #trend analysis
    path('statistics/', views.statistics, name='statistics'),
] 