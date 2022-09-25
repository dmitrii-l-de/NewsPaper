from django_filters import FilterSet, DateFilter
from .models import Post
import django.forms


class PostFilter(FilterSet):

    pub_date = DateFilter(
        lookup_expr='gte',
        widget=django.forms.DateInput(
            attrs={
                'type': 'date'
            }
        ))

    class Meta:
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            'title': ['icontains'],
            'category': ['exact'],
        }