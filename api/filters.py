from django_filters import rest_framework as filters

from core.models import Book


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    author = filters.CharFilter(field_name='author', lookup_expr='icontains')
    language = filters.CharFilter(field_name='language__name', lookup_expr='icontains')
    genre = filters.CharFilter(field_name='genre__name', lookup_expr='icontains')
    shelf = filters.NumberFilter(field_name='shelf', lookup_expr='exact')

    class Meta:
        model = Book
        fields = ['title', 'author', 'language', 'genre', 'shelf']