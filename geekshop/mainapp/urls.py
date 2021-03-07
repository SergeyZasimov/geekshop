
from django.urls import path
from mainapp import views as mainapp

app_name = 'mainappf'

urlpatterns = [
    path('', mainapp.products, name='products'),

    path('<int:pk>/', mainapp.products, name='category'),
]
