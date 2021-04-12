# b:is_django
import re
from django.db import transaction
from django.urls import reverse_lazy, reverse
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, HttpResponseRedirect

from django.views.generic.detail import DetailView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from basketapp.models import Basket
from ordersapp.models import Order, OrderItems
from ordersapp.forms import OrderItemForm

# Create your views here.


class OrderListView(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreateView(CreateView):
    model = Order
    success_url = reverse_lazy('ordersapp:orders_list')
    fields = []

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order,
                                             OrderItems,
                                             form=OrderItemForm,
                                             extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if len(basket_items):
                OrderFormSet = inlineformset_factory(Order,
                                                     OrderItems,
                                                     form=OrderItemForm,
                                                     extra=len(basket_items))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                # basket_items.delete()
            else:
                formset = OrderFormSet()

        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
                Basket.objects.filter(user=self.request.user).delete()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderReadView(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'заказ/просмотр'
        return context


class OrderUpdateView(UpdateView):
    model = Order
    success_url = reverse_lazy('ordersapp:orders_list')
    fields = []

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order,
                                             OrderItems,
                                             form=OrderItemForm,
                                             extra=1)

        if self.request.POST:
            data['orderitems'] = OrderFormSet(self.request.POST,
                                              instance=self.object)
        else:
            data['orderitems'] = OrderFormSet(instance=self.object)

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:orders_list')


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('ordersapp:orders_list'))


def get_status(request, pk, status):
    order = get_object_or_404(Order, pk=pk)
    next_status = re.search(r"[A-Z]+", status).group()
    order.status = next_status
    order.save()

    return HttpResponseRedirect(reverse('adminapp:orders_list'))
