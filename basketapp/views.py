from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import JsonResponse

from mainapp.models import Product
from basketapp.models import Basket


# Create your views here.

@login_required()
def basket(request):
    basket_items = Basket.objects.filter(user=request.user).order_by('product__category').select_related()

    context = {
        'title': 'корзина',
        'basket_items': basket_items,
    }

    return render(request, 'basketapp/basket.html', context)


@login_required
def basket_add(request, pk):

    product_item = get_object_or_404(Product, pk=pk)

    basket_item = Basket.objects.filter(product=product_item, user=request.user).first().select_related()

    if not basket_item:
        basket_item = Basket(user=request.user, product=product_item)

    basket_item.quantity += 1
    basket_item.save()

    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_item = get_object_or_404(Basket, pk=pk)
    basket_item.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=pk)

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by('product__category').select_related()

        content = {
            'basket_items': basket_items,
        }

        result = render_to_string('basketapp/includes/inc_basket_list.html', content)

        return JsonResponse({'result': result})
