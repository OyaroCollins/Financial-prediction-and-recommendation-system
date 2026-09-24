# tracker/models.py
# This file defines the database models (tables) for the finance tracking system
# Each class represents a table in the MySQL database

from django.db import models                          # Django's ORM (Object-Relational Mapping)
from django.contrib.auth.models import User           # Built-in Django User model for authentication


class Category(models.Model):
    """
    Represents income or expense categories created by users.
    Example: "Sales" (Income), "Rent" (Expense), "Transport" (Expense)
    """
    
    # Choices for the category type field
    # This restricts the type to only these two values
    TYPE_CHOICES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    ]
    
    # Primary key - auto-increments for each new category
    category_id = models.AutoField(primary_key=True)
    
    # Foreign key to the User model
    # Each category belongs to one user
    # on_delete=CASCADE means: if user is deleted, their categories are also deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Name of the category (e.g., "Rent", "Sales", "Food")
    # max_length=100 allows up to 100 characters
    category_name = models.CharField(max_length=100)
    
    # Type of category - either 'Income' or 'Expense'
    # choices=TYPE_CHOICES restricts to the values defined above
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    
    def __str__(self):
        """
        String representation of the Category object.
        This is what you see when you print a Category or view it in admin.
        Example: "Rent (Expense)"
        """
        return f"{self.category_name} ({self.type})"


class Transaction(models.Model):
    """
    Represents a financial transaction (income or expense).
    Example: Income of KES 25,000 from Sales on 2026-08-10
    """
    
    # Same choices as Category - restricts type to Income or Expense
    TYPE_CHOICES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    ]
    
    # Primary key - auto-increments for each new transaction
    transaction_id = models.AutoField(primary_key=True)
    
    # Foreign key to User
    # Each transaction belongs to one user
    # on_delete=CASCADE means: if user is deleted, their transactions are deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Foreign key to Category
    # Each transaction belongs to one category (e.g., "Rent", "Sales")
    # on_delete=CASCADE means: if category is deleted, its transactions are deleted
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    # Transaction amount (e.g., 25000.00)
    # max_digits=10 allows numbers up to 99,999,999.99
    # decimal_places=2 allows 2 decimal places (e.g., 50.75)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Date of the transaction (e.g., 2026-08-10)
    date = models.DateField()
    
    # Optional description of the transaction
    # blank=True allows empty string in forms
    # null=True allows NULL value in database
    description = models.CharField(max_length=255, blank=True, null=True)
    
    # Type of transaction - either 'Income' or 'Expense'
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    
    def __str__(self):
        """
        String representation of the Transaction object.
        Example: "Expense - 15000.00 - 2026-08-03"
        """
        return f"{self.type} - {self.amount} - {self.date}"


class Budget(models.Model):
    """
    Represents a monthly budget for a specific category.
    Example: Budget of KES 10,000 for Supplies in August 2026
    """
    
    # Primary key - auto-increments for each new budget
    budget_id = models.AutoField(primary_key=True)
    
    # Foreign key to User
    # Each budget belongs to one user
    # on_delete=CASCADE means: if user is deleted, their budgets are deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Foreign key to Category
    # Each budget is for one specific category
    # on_delete=CASCADE means: if category is deleted, its budget is deleted
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    # Budget amount limit (e.g., 10000.00)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Budget month in YYYY-MM format (e.g., "2026-08")
    # Using CharField instead of DateField because we only need year and month
    month = models.CharField(max_length=7)
    
    def __str__(self):
        """
        String representation of the Budget object.
        Example: "Supplies - 2026-08 - 10000.00"
        """
        return f"{self.category.category_name} - {self.month} - {self.amount}"