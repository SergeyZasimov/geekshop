from datetime import timedelta

from django.core.management import BaseCommand
from django.db import connection
from django.db.models import Q, F, When, Case, IntegerField, DecimalField

from adminapp.views import db_profile_by_type
from mainapp.models import Product
from ordersapp.models import OrderItems


class Command(BaseCommand):
    def handle(self, *args, **options):
        # test_products = Product.objects.filter(
        #     Q(category__name='стулья ДОМ') |
        #     Q(category__name='диваны')
        # )
        #
        # print(len(test_products))
        # print(test_products)
        # db_profile_by_type('learnDB', '', connection.queries)

        ACTION1 = 1
        ACTION2 = 2
        ACTION_EXPIRED = 3

        action1__time_delta = timedelta(hours=12)
        action2__time_delta = timedelta(days=1)

        action1__discount = 0.3
        action2__discount = 0.15
        action_expired__discount = 0.05

        action1__condition = Q(order__update__lte=F('order__created') + action1__time_delta)
        action2__condition = Q(order__update__gt=F('order__created') + action1__time_delta) & \
                             Q(order__update__lte=F('order__created') + action2__time_delta)

        action_expired__condition = Q(order__update__gt=F('order__created') + action2__time_delta)

        action1__order = When(action1__condition, then=ACTION1)
        action2__order = When(action2__condition, then=ACTION2)
        action_expired__order = When(action_expired__condition, then=ACTION_EXPIRED)

        action1__price = When(action1__condition, then=F('product__price') * F('quantity') * action1__discount)
        action2__price = When(action2__condition, then=F('product__price') * F('quantity') * action2__discount)
        action_expired__price = When(action_expired__condition,
                                     then=F('product__price') * F('quantity') * action_expired__discount)

        test_orderss = OrderItems.objects.annotate(
            action_order=Case(
                action1__order,
                action2__order,
                action_expired__order,
                output_field=IntegerField(),
            )).annotate(
            total_price=Case(
                action1__price,
                action2__price,
                action_expired__price,
                output_field=DecimalField(),
            )).order_by('action_order', 'total_price').select_related()

        for orderitem in test_orderss:
            print(f'{orderitem.action_order:2}: заказ №{orderitem.pk:3}: \
                    {orderitem.product.name:15}: скидка \
                    {abs(orderitem.total_price):6.2f} руб. | \
                    {orderitem.order.updated - orderitem.order.created}')
