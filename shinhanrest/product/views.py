from rest_framework import generics, mixins
from .models import Comment, Product
from .serializers import ProductSerializer, CommentSerializer
from .paginations import ProductLargePagination

class ProductListView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    serializer_class = ProductSerializer
    pagination_class = ProductLargePagination

    def get_queryset(self):
        products = Product.objects.all()

        # if 'name' in self.request.query_params:
        #     name = self.request.query_params['name']
        #     products = products.filter(name__contains=name)

        name = self.request.query_params.get('name')
        if name:
            products = products.filter(name__contains=name)

        return products.order_by('id')

    def get(self, request, *args, **kwargs):
        return self.list(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, args, kwargs)


class ProductDetailView(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView
):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, args, kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, args, kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, args, kwargs)


class CommentListView(
    mixins.ListModelMixin,
    generics.GenericAPIView
):
    serializer_class = CommentSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        if product_id:
            return Comment.objects.filter(product_id=product_id).order_by('-id')
        return Comment.objects.none()

    def get(self, request, *args, **kwargs):
        return self.list(request, args, kwargs)
