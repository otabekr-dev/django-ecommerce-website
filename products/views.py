import json
from django.views import View
from django.http import HttpRequest, JsonResponse
from .models import Products

class ProductView(View):

    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({'err': 'Invalid JSON'}, status=400)

        name = data.get('name')
        description = data.get('description', '')
        price = data.get('price')

        if not name:
            return JsonResponse({'err': 'Maxsulot nomini kiriting'}, status=400)
        if not price:
            return JsonResponse({'err': 'Maxsulot narxini kiriting'}, status=400)
        
        try:
            price = float(price)
        except (ValueError, TypeError):
            return JsonResponse({'err': 'Maxsulot narxini raqamda kiriting'}, status=400)

        product = Products.objects.create(
            name=name,
            description=description,
            price=price
        )

        return JsonResponse({'done': 'Maxsulot yaratildi', 'id': product.id})
    

    def get(self, request: HttpRequest) -> JsonResponse:
        products = Products.objects.all()

        product_list = [
            {
                'id': p.id,
                'name': p.name,
                'description': p.description,
                'price': str(p.price)
            } for p in products
        ]

        return JsonResponse({'products': product_list})



class ProductDetailView(View):

    def get(self, request: HttpRequest, id:int) -> JsonResponse:
        try:
            product = Products.objects.get(id=id)
            return JsonResponse({
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': str(product.price)
            })
        except Products.DoesNotExist:
            return JsonResponse({'err':'Maxsulot mavjud emas'}, status=404)

    def put(self, request: HttpRequest, id: int) -> JsonResponse:
        try:
            product = Products.objects.get(id=id)
        except Products.DoesNotExist:
            return JsonResponse({'err':'Maxsulot mavjud emas'}, status=404)

        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({'err': 'Invalid JSON'}, status=400)

        name = data.get('name', product.name)
        description = data.get('description', product.description)
        price = data.get('price', product.price)

        try:
            price = float(price)
        except (ValueError, TypeError):
            return JsonResponse({'err':'Maxsulot narxini raqamlar orqali kiriting'}, status=400)

        product.name = name
        product.description = description
        product.price = price
        product.save()

        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': str(product.price)
        })

    def delete(self, request: HttpRequest, id:int) -> JsonResponse:
        try:
            product = Products.objects.get(id=id)
        except Products.DoesNotExist:
            return JsonResponse({'err':'Maxsulot mavjud emas'}, status=404)

        product.delete()
        return JsonResponse({'done':'Maxsulot uchirildi'})