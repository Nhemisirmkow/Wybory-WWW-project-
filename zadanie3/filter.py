import django_filters

from zadanie2.models import Test, Gmina


# class GminaFilter(django_filters.FilterSet):
#     class Meta:
#         model = Gmina
#         fields = {'nazwa': ['exact', 'icontains'],
#                   'price': ['exact', 'gte', 'lte'],
#                  }

class TestFilter(django_filters.FilterSet):
    class Meta:
        model = Gmina
        fields = ['nazwa']