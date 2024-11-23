from rest_framework.serializers import ModelSerializer
from users.models import User, Payment
import django_filters


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class PaymentFilter(django_filters.FilterSet):
    class Meta:
        model = Payment
        fields = {
            'payment_date': ['exact', 'gte', 'lte'],
            'paid_course': ['exact'],
            'paid_lesson': ['exact'],
            'payment_method': ['exact'],
        }