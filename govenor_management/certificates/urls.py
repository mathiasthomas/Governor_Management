from django.urls import path
from .views import certificates_list

app_name = 'certificates'  # Replace 'your_app_name' with your actual app's name

urlpatterns = [
    path('', certificates_list, name='certificates_list'),
]
