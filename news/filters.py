from django.forms import DateInput
from django_filters import (FilterSet, CharFilter, ModelMultipleChoiceFilter, DateFilter, ModelChoiceFilter)
# импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post, Author


# создаём фильтр
class PostFilter(FilterSet):
    title = CharFilter('title', label='Заголовок содержит:', lookup_expr='icontains',)
    author = ModelChoiceFilter(field_name='author', label='Автор:', lookup_expr='exact', queryset=Author.objects.all())
    datetime = DateFilter(field_name='dateCreation', widget=DateInput(attrs={'type': 'date'}), lookup_expr='gt', label='Даты позже')
    class Meta:
        model = Post
        fields = []