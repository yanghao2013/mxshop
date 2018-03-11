from .serializers import GoodsSerializer,GoodsCategorySerializer,BannerSerializer,IndexCategorySerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import mixins
from rest_framework import generics

from .models import Goods,GoodsCategory,Banner

# class GoodsListView(APIView):
#     """
#     List all goods.
#     """
#     def get(self, request, format=None):
#         goods = Goods.objects.all()[:10]
#         serializer = GoodsSerializer(goods, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = GoodsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class GoodsListView(mixins.ListModelMixin,generics.GenericAPIView):
#     # """
#     # List all goods.
#     # """
#     queryset = Goods.objects.all()[:10]
#     serializer_class = GoodsSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework_extensions.cache.mixins import CacheResponseMixin

class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100

# class GoodsListView(generics.ListAPIView):
#     # """
#     # List all goods.
#     # """
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     pagination_class = GoodsPagination


from rest_framework import viewsets
from .filters import GoodsFilter
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication

from rest_framework.throttling import UserRateThrottle,AnonRateThrottle

class GoodsListViewset(CacheResponseMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    List all goods.
    商品列表 分页，搜索，过滤，排序
    """
    throttle_classes = (UserRateThrottle,AnonRateThrottle)
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    # authentication_classes = (TokenAuthentication,)
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    # filter_fields = ('name','shop_price')
    filter_class = GoodsFilter

    search_fields = ('name','goods_brief','goods_desc')
    ordering_fields = ('sold_num', 'shop_price')

    # 数据过滤
    # def get_queryset(self):
    #     return Goods.objects.filter(shop_price__gt=100)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num +=1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewset(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    list:商品分类列表数据
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = GoodsCategorySerializer


class BannerViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    list:商品分类列表数据
    """
    queryset = Banner.objects.all().order_by('index')
    serializer_class = BannerSerializer


class IndexCategoryViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.filter(is_tab=True,name__in=["生鲜食品","酒水饮料"])
    serializer_class = IndexCategorySerializer
