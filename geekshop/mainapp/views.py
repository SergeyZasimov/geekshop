import json
from django.conf import settings
from django.shortcuts import render

from mainapp.models import Product, ProductCategory

# Create your views here.

social_links = [
    {'class': 'social1'},
    {'class': 'social2'},
    {'class': 'social3'},
    {'class': 'social4'},
]


def main(request):

    products = Product.objects.all()[:3]

    context = {
            'title': "главная",
            'social_links': social_links,
            'products': products,
            }

    return render(request, 'mainapp/index.html', context)

def products(request, pk=None):

    products = Product.objects.all()[:4]
    links_menu = ProductCategory.objects.all()

    context = {
            'title': "продукты",
            'links_menu': links_menu,
            'social_links': social_links,
            'products': products,
            }

    return render(request, 'mainapp/products.html', context)

def contact(request):
    file_path = settings.BASE_DIR / 'static' / 'data' / 'locations.json'
    
    locations = []

    with open(file_path, encoding='utf8') as f:
        locations = json.load(f)


    context = {
            'title': "контакты",
            'social_links': social_links,
            'locations': locations,
            }

    return render(request, 'mainapp/contact.html', context)
