from django.urls import path
from .views import json_to_excel_view, register_view, login_view, logout_view, dashboard_view, pdf_to_excel_view
urlpatterns = [
    path('', dashboard_view, name='dashboard'),                 
    path('convert/', json_to_excel_view, name='json_to_excel'), 
    path('register/', register_view, name='register'),    
    path('login/', login_view, name='login'),              
    path('logout/', logout_view, name='logout'),  
    path('pdf-to-excel/', pdf_to_excel_view, name='pdf_to_excel')
]