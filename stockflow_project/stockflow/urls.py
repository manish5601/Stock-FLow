from django.urls import path
from . import views
from .views import CustomLoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('transaction-history/', views.transaction_history, name='transaction_history'),
    path('add-product/', views.add_product, name='add_product'),
    path('stock-in/<int:product_id>/', views.stock_in, name='stock_in'),
    path('stock-out/<int:product_id>/', views.stock_out, name='stock_out'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
]