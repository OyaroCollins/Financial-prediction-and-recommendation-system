# tracker/analytics.py
# This module handles the "intelligent" features of the system:
# 1. Predicting future income and expenses using Linear Regression
# 2. Generating rule-based financial recommendations

# Import required libraries
import calendar 
import pandas as pd                                    # For data manipulation and analysis
from sklearn.linear_model import LinearRegression      # For linear regression prediction
from datetime import datetime, timedelta                          # For getting current date
from django.db.models import Sum                       # For calculating totals in database queries
from .models import Transaction, Budget 
               # Import our own models


def predict_next_month(user):
    """
    Predicts next month's income and expenses using linear regression.
    
    Parameters:
        user: The logged-in user whose data we want to analyze
    
    Returns:
        A dictionary containing:
        - predicted_income: Forecasted income for next month
        - predicted_expense: Forecasted expenses for next month
        - predicted_balance: Predicted income minus predicted expense
        - error: Error message if there's not enough data
    """
    
    # Step 1: Get all transactions for this user from the database
    # We only need date, type, and amount fields
    transactions = Transaction.objects.filter(user=user).values(
        'date', 'type', 'amount'
    )
    
    # Step 2: Check if we have enough data
    # We need at least 3 transactions to make a meaningful prediction
    if len(transactions) < 3:
        return {
            'predicted_income': None,
            'predicted_expense': None,
            'predicted_balance': None,
            'error': 'Not enough data. Add at least 3 months of transactions.'
        }
    
    # Step 3: Convert the query results into a Pandas DataFrame
    # Pandas makes it easier to work with structured data
    df = pd.DataFrame(list(transactions))
    
    # Step 4: Clean and prepare the data
    # Convert date strings to actual datetime objects
    df['date'] = pd.to_datetime(df['date'])
    
    # Extract the month from each date (e.g., "2026-08-15" → "2026-08")
    df['month'] = df['date'].dt.to_period('M').astype(str)
    
    # Convert amounts from Decimal to float for calculations
    df['amount'] = df['amount'].astype(float)
    
    # Step 5: Group transactions by month and type
    # This gives us total income per month and total expenses per month
    monthly = df.groupby(['month', 'type'])['amount'].sum().reset_index()
    
    # Step 6: Separate income and expense data
    # Sort by month so the data is in chronological order
    income_data = monthly[monthly['type'] == 'Income'].sort_values('month')
    expense_data = monthly[monthly['type'] == 'Expense'].sort_values('month')
    
    # Step 7: Define a helper function to fit the model and predict
    def fit_and_predict(data):
        """
        Fits a linear regression model to monthly data and predicts next month.
        
        Parameters:
            data: DataFrame with month_index and amount columns
        
        Returns:
            Predicted amount for next month, or None if insufficient data
        """
        # Need at least 2 months of data to fit a line
        if len(data) < 2:
            return None
        
        # Create a copy so we don't modify the original
        data = data.copy()
        
        # Create a numeric index for months (0, 1, 2, ...)
        # This converts dates into numbers the model can understand
        data['month_index'] = range(len(data))
        
        # X = the month indices (independent variable)
        # y = the amounts (dependent variable - what we're predicting)
        X = data[['month_index']]
        y = data['amount']
        
        # Create and train the linear regression model
        # Linear regression finds the best-fit line through the data points
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict the next month (index = current number of months)
        # Example: if we have 6 months of data, predict month index 6
        next_index = [[len(data)]]
        prediction = model.predict(next_index)[0]
        
        # Round to 2 decimal places
        # Use max() to ensure we never predict negative amounts
        return round(max(prediction, 0), 2)
    
    # Step 8: Predict next month's income and expenses
    predicted_income = fit_and_predict(income_data)
    predicted_expense = fit_and_predict(expense_data)
    
    # Step 9: Calculate predicted balance (income - expense)
    predicted_balance = None
    if predicted_income is not None and predicted_expense is not None:
        predicted_balance = round(predicted_income - predicted_expense, 2)
    
    # Step 10: Return the results
    return {
        'predicted_income': float(predicted_income) if predicted_income is not None else None,
        'predicted_expense': float(predicted_expense) if predicted_expense is not None else None,
        'predicted_balance': float(predicted_balance) if predicted_balance is not None else None,
        'error': None
    }


def generate_recommendations(user):
    """
    Generates rule-based financial recommendations.
    
    The recommendation engine uses simple rules to analyze spending:
    - Rule 1: Flag categories where spending is 20% above average
    - Rule 2: Check if budgets have been exceeded
    - Rule 3: Calculate expense-to-income ratio
    
    Parameters:
        user: The logged-in user
    
    Returns:
        A list of recommendation dictionaries, each containing:
        - icon: Emoji representing the recommendation type
        - title: Short title for the recommendation
        - message: Detailed description
        - type: 'warning', 'alert', 'tip', or 'success'
    """
    
    # Initialize empty list to store recommendations
    recommendations = []
    
    # Get current month and year for filtering data
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # ============================================
    # RULE 1: Detect Overspending
    # Compare current month spending vs historical average per category
    # ============================================
    
    # Get current month's expenses grouped by category
    current_expenses = Transaction.objects.filter(
        user=user,
        type='Expense',
        date__month=current_month,
        date__year=current_year
    ).values('category__category_name').annotate(total=Sum('amount'))
    
    # Loop through each category's current spending
    for expense in current_expenses:
        category_name = expense['category__category_name']
        current_spending = float(expense['total'])
        
        # Get all historical spending for this category (excluding current month)
        historical = Transaction.objects.filter(
            user=user,
            type='Expense',
            category__category_name=category_name
        ).exclude(
            date__month=current_month,
            date__year=current_year
        )
        
        # Calculate total historical spending
        total_historical = historical.aggregate(total=Sum('amount'))['total']
        
        # Only proceed if we have historical data
        if total_historical:
            # Count how many months of historical data we have
            months = historical.dates('date', 'month').count()
            
            if months > 0:
                # Calculate average monthly spending for this category
                avg_spending = float(total_historical) / months
                
                # Flag if current spending is 20% above average
                if current_spending > avg_spending * 1.2:
                    # Calculate the percentage increase
                    percentage = ((current_spending - avg_spending) / avg_spending) * 100
                    
                    # Add warning recommendation
                    recommendations.append({
                        'icon': '⚠️',
                        'title': 'Overspending Detected',
                        'message': f'Your {category_name} spending is {percentage:.0f}% higher than usual this month. Current: KES {current_spending:,.0f} vs Average: KES {avg_spending:,.0f}.',
                        'type': 'warning'
                    })
    
    # ============================================
    # RULE 2: Check Budget Status
    # Compare current spending against user-defined budgets
    # ============================================
    
    # Get all budgets for the current month
    budgets = Budget.objects.filter(
        user=user,
        month=datetime.now().strftime('%Y-%m')
    )
    
    # Loop through each budget
    for budget in budgets:
        # Calculate total spending in this category for current month
        spent = Transaction.objects.filter(
            user=user,
            category=budget.category,
            type='Expense',
            date__month=current_month,
            date__year=current_year
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        spent = float(spent)
        budget_amount = float(budget.amount)
        
        # Check if budget has been exceeded
        if spent > budget_amount:
            recommendations.append({
                'icon': '🚨',
                'title': 'Budget Exceeded',
                'message': f'You have exceeded your {budget.category.category_name} budget of KES {budget_amount:,.0f}. Current spending: KES {spent:,.0f}.',
                'type': 'alert'
            })
        # Check if budget is almost used (80% or more)
        elif spent > budget_amount * 0.8:
            percentage = (spent / budget_amount) * 100
            recommendations.append({
                'icon': '⚠️',
                'title': 'Budget Almost Used',
                'message': f'You have used {percentage:.0f}% of your {budget.category.category_name} budget.',
                'type': 'warning'
            })
    
    # ============================================
    # RULE 3: Income vs Expense Ratio
    # Check if expenses are too high compared to income
    # ============================================
    
    # Calculate total income for current month
    monthly_income = float(Transaction.objects.filter(
        user=user, type='Income',
        date__month=current_month, date__year=current_year
    ).aggregate(total=Sum('amount'))['total'] or 0)
    
    # Calculate total expenses for current month
    monthly_expenses = float(Transaction.objects.filter(
        user=user, type='Expense',
        date__month=current_month, date__year=current_year
    ).aggregate(total=Sum('amount'))['total'] or 0)
    
    # Only calculate ratio if income is greater than zero (avoid division by zero)
    if monthly_income > 0:
        # Calculate expense ratio as percentage
        expense_ratio = (monthly_expenses / monthly_income) * 100
        
        # Flag if expenses are more than 80% of income
        if expense_ratio > 80:
            recommendations.append({
                'icon': '💡',
                'title': 'High Expense Ratio',
                'message': f'Your expenses are {expense_ratio:.0f}% of your income this month. Consider reducing non-essential spending.',
                'type': 'tip'
            })
    
    # ============================================
    # DEFAULT: Healthy Finances
    # If no recommendations were triggered, add positive message
    # ============================================
    if not recommendations:
        recommendations.append({
            'icon': '✅',
            'title': 'Finances Healthy',
            'message': 'Your finances look healthy. No alerts at this time.',
            'type': 'success'
        })
    
    # Return all generated recommendations
    return recommendations

def get_available_months(user):
    """
    Returns a sorted list of months (YYYY-MM format) that have transactions.
    Used to populate the date range dropdowns on the statistics page.
    
    Parameters:
        user: The logged-in user
    
    Returns:
        List of month strings sorted chronologically, e.g., ['2026-01', '2026-02', '2026-03']
    """
    # Get all transaction dates for this user
    transactions = Transaction.objects.filter(user=user).values('date')
    
    # Use a set to avoid duplicate months
    months = set()
    
    for t in transactions:
        # Extract YYYY-MM from each date
        month = t['date'].strftime('%Y-%m')
        months.add(month)
    
    # Return sorted list
    return sorted(months)


def analyze_trends(user, start_month=None, end_month=None):
    """
    Analyzes income and expense trends for a specified period.
    
    Parameters:
        user: The logged-in user
        start_month: Start month in YYYY-MM format (optional)
        end_month: End month in YYYY-MM format (optional)
    
    Returns:
        Dictionary containing:
        - monthly_data: List of months with income and expense totals
        - income_trend: 'INCREASING', 'DECREASING', or 'STABLE'
        - expense_trend: 'INCREASING', 'DECREASING', or 'STABLE'
        - income_change: Percentage change from previous month
        - expense_change: Percentage change from previous month
        - savings_rate: Savings rate for current month
        - total_income: Total income for the period
        - total_expense: Total expenses for the period
        - avg_income: Average monthly income
        - avg_expense: Average monthly expenses
        - avg_savings_rate: Average savings rate for period
        - months_count: Number of months in the period
        - best_month: Month with highest income
        - worst_month: Month with highest expenses
        - top_category: Category with highest spending
        - top_category_amount: Amount spent in top category
        - error: Error message if no data
    """
    
    # Step 1: Get all transactions for this user
    transactions = Transaction.objects.filter(user=user).values(
        'date', 'type', 'amount', 'category__category_name'
    )
    
    # Step 2: Filter by date range if provided
    if start_month:
        # Filter transactions on or after start_month
        transactions = transactions.filter(date__gte=start_month + '-01')
    
    if end_month:
        # Parse year and month from the string
        year, month = end_month.split('-')
        year = int(year)
        month = int(month)
        
        # Get the last day of the month using calendar module
        last_day = calendar.monthrange(year, month)[1]
        
        # Build correct end date (e.g., "2026-02-28")
        end_date = f"{end_month}-{last_day:02d}"
        
        # Filter transactions on or before the last day of the month
        transactions = transactions.filter(date__lte=end_date)
    
    # Step 3: Check if we have data
    if len(transactions) == 0:
        return {
            'monthly_data': [],
            'income_trend': None,
            'expense_trend': None,
            'income_change': None,
            'expense_change': None,
            'savings_rate': None,
            'total_income': 0,
            'total_expense': 0,
            'avg_income': 0,
            'avg_expense': 0,
            'avg_savings_rate': None,
            'months_count': 0,
            'best_month': None,
            'worst_month': None,
            'top_category': None,
            'top_category_amount': None,
            'error': 'No transactions found for the selected period.'
        }
    
    # Step 4: Convert to Pandas DataFrame
    df = pd.DataFrame(list(transactions))
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M').astype(str)
    df['amount'] = df['amount'].astype(float)
    
    # Step 5: Group by month and type
    monthly = df.groupby(['month', 'type'])['amount'].sum().reset_index()
    
    # Step 6: Create pivot table (rows = months, columns = Income/Expense)
    pivot = monthly.pivot(index='month', columns='type', values='amount').fillna(0)
    
    # Ensure both columns exist
    if 'Income' not in pivot.columns:
        pivot['Income'] = 0
    if 'Expense' not in pivot.columns:
        pivot['Expense'] = 0
    
    # Step 7: Sort chronologically
    pivot = pivot.sort_index()
    
    # Step 8: Prepare monthly data for charts
        # Step 8: Prepare monthly data for charts
    monthly_data = []
    for month, row in pivot.iterrows():
        monthly_data.append({
            'month': str(month),
            'income': float(round(row['Income'], 2)),
            'expense': float(round(row['Expense'], 2)),
        })
    
    # Step 9: Analyze income trend
    income_values = pivot['Income'].tolist()
    if len(income_values) >= 2:
        if income_values[-1] > income_values[-2]:
            income_trend = 'INCREASING'
        elif income_values[-1] < income_values[-2]:
            income_trend = 'DECREASING'
        else:
            income_trend = 'STABLE'
        
        # Calculate percentage change
        if income_values[-2] > 0:
            income_change = round(((income_values[-1] - income_values[-2]) / income_values[-2]) * 100, 1)
        else:
            income_change = None
    else:
        income_trend = 'STABLE'
        income_change = None
    
    # Step 10: Analyze expense trend
    expense_values = pivot['Expense'].tolist()
    if len(expense_values) >= 2:
        if expense_values[-1] > expense_values[-2]:
            expense_trend = 'INCREASING'
        elif expense_values[-1] < expense_values[-2]:
            expense_trend = 'DECREASING'
        else:
            expense_trend = 'STABLE'
        
        # Calculate percentage change
        if expense_values[-2] > 0:
            expense_change = round(((expense_values[-1] - expense_values[-2]) / expense_values[-2]) * 100, 1)
        else:
            expense_change = None
    else:
        expense_trend = 'STABLE'
        expense_change = None
    
    # Step 11: Calculate totals
    total_income = round(pivot['Income'].sum(), 2)
    total_expense = round(pivot['Expense'].sum(), 2)
    
    # Step 12: Calculate averages
    months_count = len(pivot)
    
    if months_count > 0:
        avg_income = round(total_income / months_count, 2)
        avg_expense = round(total_expense / months_count, 2)
    else:
        avg_income = 0
        avg_expense = 0
    
    # Step 13: Calculate average savings rate
    if total_income > 0:
        avg_savings_rate = round(((total_income - total_expense) / total_income) * 100, 1)
    else:
        avg_savings_rate = None
    
    # Step 14: Calculate current month savings rate
    current_income = income_values[-1] if income_values else 0
    current_expense = expense_values[-1] if expense_values else 0
    
    if current_income > 0:
        savings_rate = round(((current_income - current_expense) / current_income) * 100, 1)
    else:
        savings_rate = None
    
    # Step 15: Find best month (highest income)
    if total_income > 0 and len(income_values) > 0:
        best_month_index = income_values.index(max(income_values))
        best_month = pivot.index[best_month_index]
    else:
        best_month = None
    
    # Step 16: Find worst month (highest expenses)
    if total_expense > 0 and len(expense_values) > 0:
        worst_month_index = expense_values.index(max(expense_values))
        worst_month = pivot.index[worst_month_index]
    else:
        worst_month = None
    
    # Step 17: Find top spending category for the period
    expense_df = df[df['type'] == 'Expense']
    
    if len(expense_df) > 0:
        category_totals = expense_df.groupby('category__category_name')['amount'].sum()
        top_category = category_totals.idxmax()
        top_category_amount = round(category_totals.max(), 2)
    else:
        top_category = None
        top_category_amount = None
    
    # Step 18: Return complete results
    return {
        'monthly_data': monthly_data,
        'income_trend': income_trend,
        'expense_trend': expense_trend,
        'income_change': float(income_change) if income_change is not None else None,
        'expense_change': float(expense_change) if expense_change is not None else None,
        'savings_rate': float(savings_rate) if savings_rate is not None else None,
        'total_income': float(total_income),
        'total_expense': float(total_expense),
        'avg_income': float(avg_income),
        'avg_expense': float(avg_expense),
        'avg_savings_rate': float(avg_savings_rate) if avg_savings_rate is not None else None,
        'months_count': int(months_count),
        'best_month': str(best_month) if best_month is not None else None,
        'worst_month': str(worst_month) if worst_month is not None else None,
        'top_category': top_category,
        'top_category_amount': float(top_category_amount) if top_category_amount is not None else None,
        'error': None
    }