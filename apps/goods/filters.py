# _*_ coding:utf-8 _*_

__author__ = 'yanghao'
__date__ = '2018/1/6 17:17'
from django_filters import rest_framework as filters
from django.db.models import Q

from .models import Goods


class GoodsFilter(filters.FilterSet):
    name = filters.CharFilter(name='name',lookup_expr='icontains')
    pricemin = filters.NumberFilter(name="shop_price", lookup_expr='gte')
    pricemax = filters.NumberFilter(name="shop_price", lookup_expr='lte')
    top_category = filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self,queryset,name,value):
        return queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['name','pricemin', 'pricemax','is_hot','is_new']

