# tracker/admin.py
# Registers our models with Django's built-in admin panel
# This allows us to manage data through /admin/

from django.contrib import admin
from .models import Category, Transaction, Budget

# Register Category model
admin.site.register(Category)

# Register Transaction model
admin.site.register(Transaction)

# Register Budget model
admin.site.register(Budget)