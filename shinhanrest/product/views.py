from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product


class ProductListView(APIView):
    def post(self, request, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):
        ret = []
        products = Product.objects.all().order_by('id')

        for product in products:
            p = {
                'name': product.name,
                'price': product.price,
                'product_type': product.product_type,
            }
            ret.append(p)

        return Response(ret)


class ProductDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        product = Product.objects.get(pk=pk)

        ret = {
            'name': product.name,
            'price': product.price,
            'product_type': product.product_type,
        }

        return Response(ret)
