import json
import random

from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from mainapp.models import Product, ProductCategory
from basketapp.models import Basket

# Create your views here.

social_links = [
    {'class': 'social1'},
    {'class': 'social2'},
    {'class': 'social3'},
    {'class': 'social4'},
]


# def get_basket(user):
#    if user.is_authenticated:
#        return Basket.objects.filter(user=user)
#        #basket = sum(list(Basket.objects.filter(user=request.user).values_list('quantity', flat=True)))
#    return []

def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related("category")
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related("category")


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_ordered_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def get_hot_product():
    product_list = get_products()
    return random.sample(list(product_list), 1)[0]


def get_same_products(hot_product):
    same_products = get_products_in_category_ordered_by_price(pk=hot_product.category.pk).exclude(pk=hot_product.pk)[:3]
    return same_products


def main(request):
    products = get_products()[:3]

    context = {
        'title': "главная",
        'social_links': social_links,
        'products': products,
        # 'basket': get_basket(request.user),
    }

    return render(request, 'mainapp/index.html', context)


def products(request, pk=None, page=1):
    title = "продукты"

    links_menu = get_links_menu()

    if pk is not None:
        if pk == 0:
            products = get_products_ordered_by_price()
            category_item = {'name': 'все', 'pk': 0}
        else:
            category_item =get_category(pk)
            products = get_products_in_category_ordered_by_price(pk)

        paginator = Paginator(products, 2)

        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        content = {
            'title': title,
            'links_menu': links_menu,
            'social_links': social_links,
            'category': category_item,
            'products': products_paginator,
            # 'basket': get_basket(request.user),
        }

        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    products = get_same_products(hot_product)
    context = {
        'links_menu': links_menu,
        'social_links': social_links,
        'hot_product': hot_product,
        'products': products,
        # 'basket': get_basket(request.user),
    }

    return render(request, 'mainapp/products.html', context)


def product(request, pk):
    links_menu = get_links_menu()

    content = {
        'title': 'продукт',
        'product': get_product(pk),
        # 'basket': get_basket(request.user),
        'links_menu': links_menu,
        'social_links': social_links,
    }

    return render(request, 'mainapp/product.html', content)


def contact(request):
    file_path = settings.BASE_DIR / 'static' / 'data' / 'locations.json'
    locations = []
    if settings.LOW_CACHE:
        key = 'locations'
        locations = cache.get(key)
        if locations is None:
            with open(file_path, encoding='utf8') as f:
                locations = json.load(f)
            cache.set(key, locations)
        else:
            with open(file_path, encoding='utf8') as f:
                locations = json.load(f)

    context = {
        'title': "контакты",
        'social_links': social_links,
        'locations': locations,
        # 'basket': get_basket(request.user),
    }

    return render(request, 'mainapp/contact.html', context)
