from django.urls import path
from .views import json_to_excel_view, register_view, login_view, logout_view, dashboard_view

urlpatterns = [
    path('', dashboard_view, name='dashboard'),                 # Root URL now goes to dashboard
    path('convert/', json_to_excel_view, name='json_to_excel'),  # Conversion page
    path('register/', register_view, name='register'),     # Registration page
    path('login/', login_view, name='login'),              # Login page
    path('logout/', logout_view, name='logout'),           # Logout action
]