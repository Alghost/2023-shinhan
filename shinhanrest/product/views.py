from rest_framework import generics, mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Comment, Like, Product
from .serializers import (
    ProductSerializer,
    CommentSerializer,
    CommentCreateSerializer,
    LikeCreateSerializer,
)
from .paginations import ProductLargePagination

class ProductListView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    serializer_class = ProductSerializer
    pagination_class = ProductLargePagination
    # permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        products = Product.objects.all().prefetch_related('comment_set')
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
            return Comment.objects.filter(product_id=product_id) \
                    .select_related('member', 'product') \
                    .order_by('-id')
        return Comment.objects.none()

    def get(self, request, *args, **kwargs):
        return self.list(request, args, kwargs)


class CommentCreateView(
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    serializer_class = CommentCreateSerializer

    def get_queryset(self):
        return Comment.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, args, kwargs)


class LikeCreateView(
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    serializer_class = LikeCreateSerializer

    def get_queryset(self):
        return Like.objects.all()

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product')

        if Like.objects.filter(member=request.user, product_id=product_id).exists():
            Like.objects.filter(member=request.user, product_id=product_id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return self.create(request, args, kwargs)