
from django.urls import path
from django.views.decorators.cache import cache_page

from mainapp import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.products, name='products'),
    path('<int:pk>/', mainapp.products, name='category'),
    path('<int:pk>/ajax/', cache_page(3600)(mainapp.products_ajax)),
    path('<int:pk>/<int:page>/', mainapp.products, name='page'),
    path('<int:pk>/<int:page>/ajax/', cache_page(3600)(mainapp.products_ajax)),
    path('product/<int:pk>/', mainapp.product, name='product'),
]
