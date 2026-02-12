import json
from django.views import View
from django.http import HttpRequest, JsonResponse
from .models import Order, OrderItem
from products.models import Products
from django.contrib.auth import get_user_model

User = get_user_model()

class OrderView(View):

    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({'err': 'Invalid JSON'}, status=400)

        user_id = data.get('user_id')
        items = data.get('items')  

        if not user_id or not items:
            return JsonResponse({'err': 'User ID va items required'}, status=400)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'err': 'User not found'}, status=404)

        order = Order.objects.create(user=user, total=0)
        total = 0

        for i in items:
            try:
                product = Products.objects.get(id=i['product_id'])
                quantity = int(i.get('quantity', 1))
                price = product.price * quantity
                total += price

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )
            except Products.DoesNotExist:
                continue

        order.total = total
        order.save()

        return JsonResponse({'done': f'Order {order.id} created', 'total': str(order.total)})


    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.all()
        order_list = []

        for o in orders:
            items = [{'product': item.product.name, 'quantity': item.quantity, 'price': str(item.price)}
                     for item in o.items.all()]
            order_list.append({
                'id': o.id,
                'user': o.user.username,
                'total': str(o.total),
                'items': items
            })

        return JsonResponse({'orders': order_list})
