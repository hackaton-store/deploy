from django_filters import rest_framework as filters
from product.models import Car



class CarFilter(filters.FilterSet):
    price = filters.RangeFilter()
    release = filters.RangeFilter()


    class Meta:
        model = Car
        # fields = ['price', 'release']
        fields = {
            'brand': ['exact'],
            'color': ['exact'],
            'title': ['icontains'],
            'description': ['icontains'],
        }


