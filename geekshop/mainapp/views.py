import json
import random
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


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
        #basket = sum(list(Basket.objects.filter(user=request.user).values_list('quantity', flat=True)))
    return []


def get_hot_product():
    product_list = Product.objects.all()
    return random.sample(list(product_list), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products


def main(request):

    products = Product.objects.all()[:3]

    context = {
            'title': "главная",
            'social_links': social_links,
            'products': products,
            'basket': get_basket(request.user),
            }

    return render(request, 'mainapp/index.html', context)


def products(request, pk=None):

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
            'basket': get_basket(request.user),
        }
        
        return render(request, 'mainapp/products_list.html', content)


    hot_product = get_hot_product()
    products = get_same_products(hot_product)
    context = {
            'links_menu': links_menu,
            'social_links': social_links,
            'hot_product': hot_product,
            'products': products,
            'basket': get_basket(request.user),
            }

    return render(request, 'mainapp/products.html', context)

def product(request, pk):
    
    links_menu = ProductCategory.objects.all()

    content = {
        'title': 'продукт',
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user),
        'links_menu': links_menu,
        'social_links': social_links,
    }

    return render(request, 'mainapp/product.html', content)

def contact(request):
    file_path = settings.BASE_DIR / 'static' / 'data'  /'locations.json'
    
    locations = []

    with open(file_path, encoding='utf8') as f:
        locations = json.load(f)


    context = {
            'title': "контакты",
            'social_links': social_links,
            'locations': locations,
            'basket': get_basket(request.user),
            }

    return render(request, 'mainapp/contact.html', context)
