from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Transaction, Category, UserProfile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'quantity', 'price']  # Adjust fields as needed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize widgets for quantity and price
        self.fields['quantity'].widget = forms.NumberInput(attrs={
            'class': 'form-control form-control-lg shadow-sm',
            'placeholder': 'Enter quantity',
            'min': '0',  # Optional: Prevent negative quantities
        })
        self.fields['price'].widget = forms.NumberInput(attrs={
            'class': 'form-control form-control-lg shadow-sm',
            'placeholder': 'Enter price',
            'step': '0.01',  # Allow decimal values for price
            'min': '0',  # Optional: Prevent negative prices
        })
        # Ensure category uses a dropdown (this is the default, but we can customize if needed)
        self.fields['category'].widget.attrs.update({
            'class': 'form-control form-control-lg shadow-sm',
        })

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['quantity']

class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, required=True, label="Email Address")

    class Meta:
        model = UserProfile
        fields = ['full_name', 'profile_picture', 'bio', 'email']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email