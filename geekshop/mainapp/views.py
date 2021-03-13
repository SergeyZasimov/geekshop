import json
from django.conf import settings
from django.shortcuts import render, get_object_or_404

from mainapp.models import Product, ProductCategory
from basketapp.models import Basket

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

    basket = 0
    if request.user.is_authenticated:
        basket = sum(list(Basket.objects.filter(user=request.user).values_list('quantity', flat=True)))

    title =  "продукты"

    links_menu = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category_item = {'name': 'все', 'pk': 0}
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category=category_item)

        content = {
            'title': title,
            'links_menu': links_menu,
            'social_links': social_links,
            'category': category_item,
            'products': products,
            'basket': basket,
        }
        
        return render(request, 'mainapp/products_list.html', content)


    products = Product.objects.all()
    context = {
            'title': title,
            'links_menu': links_menu,
            'social_links': social_links,
            'products': products,
            'basket': basket,
            }

    return render(request, 'mainapp/products.html', context)


def contact(request):
    file_path = settings.BASE_DIR / 'static' / 'data'  /'locations.json'
    
    locations = []

    with open(file_path, encoding='utf8') as f:
        locations = json.load(f)


    context = {
            'title': "контакты",
            'social_links': social_links,
            'locations': locations,
            }

    return render(request, 'mainapp/contact.html', context)
