import json
from geekshop.settings import BASE_DIR
from django.shortcuts import render

# Create your views here.

social_links = [
    {'class': 'social1'},
    {'class': 'social2'},
    {'class': 'social3'},
    {'class': 'social4'},
]


def main(request):
    context = {
            'title': "главная",
            'social_links': social_links,
            }
    return render(request, 'mainapp/index.html', context)

def products(request):
    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]
    context = {
            'title': "продукты",
            'links_menu': links_menu,
            'social_links': social_links,
            }
    return render(request, 'mainapp/products.html', context)

def contact(request):
    file_path = BASE_DIR / 'mainapp' / 'templates' / 'mainapp' / 'data' / 'locations.json'

    with open(file_path, encoding='utf8') as f:
        data = json.load(f)

        locations = data['locations']

    context = {
            'title': "контакты",
            'social_links': social_links,
            'locations': locations,
            }
    return render(request, 'mainapp/contact.html', context)
