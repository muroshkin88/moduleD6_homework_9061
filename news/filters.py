from django_filters import FilterSet
from .models import Post


# создаём фильтр
class NewsFilter(FilterSet):
    class Meta:
        model = Post
        fields = {'dateCreat': ['lte'],
                  'author__authorUser__username': ['icontains'],
                  }