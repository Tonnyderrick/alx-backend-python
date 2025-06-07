import django_filters
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    timestamp__gte = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    timestamp__lte = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'timestamp__gte', 'timestamp__lte']
