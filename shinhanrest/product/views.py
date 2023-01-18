from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product


class ProductListView(APIView):
    def post(self, request, *args, **kwargs):
        # 전달한 값 받아오기
        name = request.data.get('name')
        price = request.data.get('price')
        product_type= request.data.get('product_type')

        # Product 객체 생성
        product = Product(
            name=name,
            price=price,
            product_type=product_type
        )
        # 객체의 save함수를 사용하여 Database에 저장
        product.save() # Primary key 가 이 때 만들어짐!

        return Response({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'product_type': product.product_type,           
        }, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        ret = []
        # QuerySet
        products = Product.objects.all() # 이 순간 DB에서 가져오지 않음.

        if 'price' in request.query_params:
            price = request.query_params['price']
            products = products.filter(price__lte=price) # 이 순간 DB에서 가져오지 않음.

        if 'name' in request.query_params:
            name = request.query_params['name']
            products = products.filter(name__contains=name) # 이 순간 DB에서 가져오지 않음.

        products = products.order_by('id') # 이 순간 DB에서 가져오지 않음.

        for product in products:
            p = {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'product_type': product.product_type,
            }
            ret.append(p)

        return Response(ret)


class ProductDetailView(APIView):
    def put(self, request, pk, *args, **kwargs):
        product = Product.objects.get(pk=pk)

        # if 'name' in request.data:
        #     product.name = request.data['name']

        # if 'price' in request.data:
        #     product.price = request.data['price']

        # if 'product_type' in request.data:
        #     product.product_type = request.data['product_type']


        dirty = False
        for field, value in request.data.items():
            if field not in [f.name for f in product._meta.get_fields()]:
                continue

            dirty = dirty or (value != getattr(product, field))
            setattr(product, field, value)

        if dirty:
            product.save()

        return Response()

    def delete(self, request, pk, *args, **kwargs):
        if Product.objects.filter(pk=pk).exists():
            product = Product.objects.get(pk=pk)
            product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, *args, **kwargs):
        # 1. get 하기 전에 exists()로 확인하고 가져오기
        # 2. get 할 때 예외처리 하기

        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        ret = {
            'name': product.name,
            'price': product.price,
            'product_type': product.product_type,
        }

        return Response(ret)
