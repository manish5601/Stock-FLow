from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from .forms import SignUpForm, ProductForm, TransactionForm, UserProfileForm
from .models import Product, Transaction, Category, UserProfile
from django.db.models import Count, Sum
from django.contrib import messages

# Helper function to check if user is superuser
def superuser_required(user):
    return user.is_superuser

# Home View
def home(request):
    return render(request, 'home.html')

# Login View
class CustomLoginView(LoginView):
    template_name = 'login.html'

# Signup View
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# Logout View (combined, with messages)
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('home')

# Profile View
@login_required
def profile(request):
    user = request.user
    user_profile = getattr(user, 'userprofile', None)
    context = {
        'user': user,
        'user_profile': user_profile,
    }
    return render(request, 'profile.html', context)

# Dashboard View
@login_required
def dashboard(request):
    products = Product.objects.all()
    product_names = [product.name for product in products]
    product_quantities = [product.quantity for product in products]
    print("Product Names:", product_names)
    print("Product Quantities:", product_quantities)

    categories = Product.objects.values('category__name').annotate(count=Count('id'))
    category_names = [category['category__name'] for category in categories]
    category_counts = [category['count'] for category in categories]
    print("Category Names:", category_names)
    print("Category Counts:", category_counts)

    end_date = timezone.now()
    start_date = end_date - timezone.timedelta(days=7)
    transactions = Transaction.objects.filter(date__range=[start_date, end_date]).order_by('date')
    dates = [transaction.date.strftime('%Y-%m-%d') for transaction in transactions]
    quantities = [transaction.quantity for transaction in transactions]
    print("Dates:", dates)
    print("Quantities:", quantities)

    context = {
        'products': products,
        'product_names': product_names,
        'product_quantities': product_quantities,
        'category_names': category_names,
        'category_counts': category_counts,
        'dates': dates,
        'quantities': quantities,
    }
    return render(request, 'dashboard.html', context)

# Transaction History View
@login_required
def transaction_history(request):
    transactions = Transaction.objects.all().order_by('-date')
    return render(request, 'transaction_history.html', {'transactions': transactions})

# Add Product View
@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

# Stock In View
@login_required
def stock_in(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            product.quantity += quantity
            product.save()
            Transaction.objects.create(
                product=product,
                user=request.user,
                type='IN',
                quantity=quantity,
                date=timezone.now()
            )
            return redirect('dashboard')
    else:
        form = TransactionForm()
    return render(request, 'stock_transaction.html', {'form': form, 'product': product, 'type': 'Stock In'})

# Stock Out View
@login_required
def stock_out(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if quantity <= product.quantity:
                product.quantity -= quantity
                product.save()
                Transaction.objects.create(
                    product=product,
                    user=request.user,
                    type='OUT',
                    quantity=quantity,
                    date=timezone.now()
                )
                return redirect('dashboard')
            else:
                form.add_error('quantity', 'Not enough stock available.')
    else:
        form = TransactionForm()
    return render(request, 'stock_transaction.html', {'form': form, 'product': product, 'type': 'Stock Out'})

# Edit Product View (Superuser only)
@login_required
@user_passes_test(superuser_required, login_url='dashboard')
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product '{product.name}' updated successfully.")
            return redirect('dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form, 'product': product})

# Delete Product View (Superuser only)
@login_required
@user_passes_test(superuser_required, login_url='dashboard')
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_name = product.name
    product.delete()
    messages.success(request, f"Product '{product_name}' deleted successfully.")
    return redirect('dashboard')

# Privacy Policy View
def privacy_policy(request):
    return render(request, 'privacy_policy.html')

# Terms of Service View
def terms_of_service(request):
    return render(request, 'terms_of_service.html')

# Contact Us View
def contact_us(request):
    return render(request, 'contact_us.html')

# Edit Profile View
@login_required
def edit_profile(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile, user=user)
        if form.is_valid():
            user.email = form.cleaned_data['email']
            user.save()
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile, user=user)
    context = {
        'form': form,
    }
    return render(request, 'edit_profile.html', context)