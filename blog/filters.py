import django_filters
from django import forms
from .models import Post

class PostFilter(django_filters.FilterSet):
    date_range = django_filters.DateRangeFilter(
        field_name='published_date', 
        widget=forms.Select(attrs={'onchange': 'this.form.submit()'}),
        label='Data')

    class Meta:
        model = Post
        fields = []