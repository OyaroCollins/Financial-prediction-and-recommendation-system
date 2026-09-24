# tracker/views.py
# This file contains the view functions that handle user requests
# Each view receives a request, processes it, and returns a response

# Import Django shortcuts for common operations
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required    # Requires login for certain pages
from django.contrib import messages                          # For success/error messages
from django.db.models import Sum                             # For calculating totals
from datetime import datetime                                # For getting current date

# Import our models
from .models import Category, Transaction, Budget

# Import our analytics functions
from .analytics import predict_next_month, generate_recommendations, analyze_trends, get_available_months


@login_required
def dashboard(request):
    """
    Displays the main dashboard with summary cards, charts, and recent transactions.
    """
    
    # Get current month and year for filtering
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Calculate total income for current month
    # If no income exists, default to 0
    total_income = Transaction.objects.filter(
        user=request.user,
        type='Income',
        date__month=current_month,
        date__year=current_year
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Calculate total expenses for current month
    total_expenses = Transaction.objects.filter(
        user=request.user,
        type='Expense',
        date__month=current_month,
        date__year=current_year
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Calculate current balance (income minus expenses)
    current_balance = total_income - total_expenses
    
    # Get the 5 most recent transactions (ordered by date, newest first)
    recent_transactions = Transaction.objects.filter(
        user=request.user
    ).order_by('-date', '-transaction_id')[:5]
    
    # Prepare context data to pass to the template
    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'current_balance': current_balance,
        'recent_transactions': recent_transactions,
    }
    
    # Render the dashboard template with the context data
    return render(request, 'tracker/dashboard.html', context)


@login_required
def transaction_list(request):
    """
    Displays all transactions for the logged-in user.
    Supports filtering by type, category, and month.
    """
    
    # Start with all transactions for this user
    transactions = Transaction.objects.filter(user=request.user).order_by('-date', '-transaction_id')
    
    # Get filter parameters from the URL query string
    filter_type = request.GET.get('type', '')            # e.g., "Income" or "Expense"
    filter_category = request.GET.get('category', '')     # e.g., "Rent"
    filter_month = request.GET.get('month', '')           # e.g., "2026-08"
    
    # Apply type filter if provided
    if filter_type:
        transactions = transactions.filter(type=filter_type)
    
    # Apply category filter if provided
    if filter_category:
        transactions = transactions.filter(category__category_name=filter_category)
    
    # Apply month filter if provided
    if filter_month:
        transactions = transactions.filter(date__startswith=filter_month)
    
    # Get all categories for the filter dropdown
    categories = Category.objects.filter(user=request.user)
    
    # Prepare context
    context = {
        'transactions': transactions,
        'categories': categories,
        'filter_type': filter_type,
        'filter_category': filter_category,
        'filter_month': filter_month,
    }
    
    return render(request, 'tracker/transactions.html', context)


@login_required
def add_transaction(request):
    """
    Handles creation of a new transaction.
    GET: Displays the add transaction form.
    POST: Processes the form and saves the transaction.
    """
    
    # Check if form was submitted (POST request)
    if request.method == 'POST':
        # Get form data from the request
        transaction_type = request.POST.get('type')
        category_id = request.POST.get('category')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        description = request.POST.get('description', '')
        
        # Fetch the Category object from database
        category = get_object_or_404(Category, pk=category_id, user=request.user)
        
        # Create the new transaction in the database
        Transaction.objects.create(
            user=request.user,
            category=category,
            amount=amount,
            date=date,
            description=description,
            type=transaction_type
        )
        
        # Show success message to user
        messages.success(request, 'Transaction added successfully.')
        
        # Redirect to transaction list page
        return redirect('transaction_list')
    
    # GET request - display the form
    # Get user's categories for the dropdown
    categories = Category.objects.filter(user=request.user)
    
    context = {'categories': categories}
    return render(request, 'tracker/add_transaction.html', context)


@login_required
def edit_transaction(request, transaction_id):
    """
    Handles editing an existing transaction.
    GET: Displays the edit form with pre-filled data.
    POST: Updates the transaction in the database.
    """
    
    # Get the transaction to edit, or show 404 if not found
    # Also verify the transaction belongs to the logged-in user
    transaction = get_object_or_404(
        Transaction, 
        pk=transaction_id, 
        user=request.user
    )
    
    # Check if form was submitted
    if request.method == 'POST':
        # Update transaction fields from form data
        transaction.type = request.POST.get('type')
        transaction.category_id = request.POST.get('category')
        transaction.amount = request.POST.get('amount')
        transaction.date = request.POST.get('date')
        transaction.description = request.POST.get('description', '')
        transaction.save()  # Save changes to database
        
        # Show success message
        messages.success(request, 'Transaction updated successfully.')
        
        # Redirect to transaction list
        return redirect('transaction_list')
    
    # GET request - display edit form with current data
    categories = Category.objects.filter(user=request.user)
    
    context = {
        'transaction': transaction,
        'categories': categories,
    }
    return render(request, 'tracker/edit_transaction.html', context)


@login_required
def delete_transaction(request, transaction_id):
    """
    Handles deletion of a transaction.
    """
    
    # Get the transaction to delete
    # Verify it belongs to the logged-in user
    transaction = get_object_or_404(
        Transaction, 
        pk=transaction_id, 
        user=request.user
    )
    
    # Delete from database
    transaction.delete()
    
    # Show success message
    messages.success(request, 'Transaction deleted successfully.')
    
    # Redirect back to transaction list
    return redirect('transaction_list')


@login_required
def categories(request):
    """
    Handles category management.
    GET: Displays category list and add form.
    POST: Adds a new category.
    """
    
    # Check if form was submitted
    if request.method == 'POST':
        # Get form data
        category_name = request.POST.get('category_name')
        category_type = request.POST.get('type')
        
        # Create new category in database
        Category.objects.create(
            user=request.user,
            category_name=category_name,
            type=category_type
        )
        
        # Show success message
        messages.success(request, 'Category added successfully.')
        
        # Redirect back to categories page
        return redirect('categories')
    
    # GET request - display categories
    income_categories = Category.objects.filter(user=request.user, type='Income')
    expense_categories = Category.objects.filter(user=request.user, type='Expense')
    
    context = {
        'income_categories': income_categories,
        'expense_categories': expense_categories,
    }
    return render(request, 'tracker/categories.html', context)


@login_required
def delete_category(request, category_id):
    """
    Handles deletion of a category.
    """
    
    # Get the category to delete
    # Verify it belongs to the logged-in user
    category = get_object_or_404(
        Category, 
        pk=category_id, 
        user=request.user
    )
    
    # Delete from database
    category.delete()
    
    # Show success message
    messages.success(request, 'Category deleted successfully.')
    
    # Redirect back to categories page
    return redirect('categories')


@login_required
def predictions(request):
    """
    Displays financial predictions using linear regression.
    """
    
    # Call the prediction function from analytics.py
    result = predict_next_month(request.user)
    
    # Prepare context with prediction results
    context = {
        'predicted_income': result['predicted_income'],
        'predicted_expense': result['predicted_expense'],
        'predicted_balance': result['predicted_balance'],
        'error': result['error'],
    }
    
    return render(request, 'tracker/predictions.html', context)


@login_required
def recommendations(request):
    """
    Displays rule-based financial recommendations.
    """
    
    # Call the recommendation function from analytics.py
    recs = generate_recommendations(request.user)
    
    # Prepare context
    context = {
        'recommendations': recs,
    }
    
    return render(request, 'tracker/recommendations.html', context)


@login_required
def budgets(request):
    """
    Handles budget management.
    GET: Displays budget list and add form.
    POST: Adds a new budget.
    """
    
    # Check if form was submitted
    if request.method == 'POST':
        # Get form data
        category_id = request.POST.get('category')
        amount = request.POST.get('amount')
        month = request.POST.get('month')
        
        # Get the category object
        category = get_object_or_404(Category, pk=category_id, user=request.user)
        
        # Create new budget
        Budget.objects.create(
            user=request.user,
            category=category,
            amount=amount,
            month=month
        )
        
        messages.success(request, 'Budget added successfully.')
        return redirect('budgets')
    
    # GET request - display budgets
    budgets = Budget.objects.filter(user=request.user).order_by('-month')
    categories = Category.objects.filter(user=request.user, type='Expense')
    
    context = {
        'budgets': budgets,
        'categories': categories,
    }
    return render(request, 'tracker/budgets.html', context)

@login_required
def delete_budget(request, budget_id):
    """
    Handles deletion of a budget.
    Parameters:
        budget_id: The ID of the budget to delete
    """
    # Get the budget to delete
    # Verify it belongs to the logged-in user
    budget = get_object_or_404(Budget, pk=budget_id, user=request.user)
    
    # Delete from database
    budget.delete()
    
    # Show success message
    messages.success(request, 'Budget deleted successfully.')
    
    # Redirect back to budgets page
    return redirect('budgets')

def home(request):
    """
    Displays the landing/home page.
    """
    return render(request, 'tracker/home.html')

@login_required
def statistics(request):
    """
    Displays statistical analysis of income and expense trends
    for a user-selected date range.
    """
    # Get date range from URL query parameters
    start_month = request.GET.get('start_month', None)
    end_month = request.GET.get('end_month', None)
    
    # Call trend analysis with selected range
    result = analyze_trends(request.user, start_month=start_month, end_month=end_month)
    
    # Get list of months with data for dropdowns
    available_months = get_available_months(request.user)
    
    context = {
        'monthly_data': result['monthly_data'],
        'income_trend': result['income_trend'],
        'expense_trend': result['expense_trend'],
        'income_change': result['income_change'],
        'expense_change': result['expense_change'],
        'savings_rate': result['savings_rate'],
        'total_income': result['total_income'],
        'total_expense': result['total_expense'],
        'avg_income': result['avg_income'],
        'avg_expense': result['avg_expense'],
        'avg_savings_rate': result['avg_savings_rate'],
        'months_count': result['months_count'],
        'best_month': result['best_month'],
        'worst_month': result['worst_month'],
        'top_category': result['top_category'],
        'top_category_amount': result['top_category_amount'],
        'error': result['error'],
        'start_month': start_month,
        'end_month': end_month,
        'available_months': available_months,
    }
    
    return render(request, 'tracker/statistics.html', context)