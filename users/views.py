from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, filters
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework import generics
from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer, PaymentFilter
from rest_framework.filters import OrderingFilter
from users.services import create_stripe_session, create_stripe_product, create_stripe_price


class UserViewSet(viewsets.ModelViewSet):
    """Список всех пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]

class UserCreateAPIView(CreateAPIView):
    """Контроллер для регистрации пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ('date',)


class PaymentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer



class PaymentCreateAPIView(CreateAPIView):
    """Эндпоинт создания оплаты"""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save()
        payment.user = self.request.user
        stripe_product_id = create_stripe_product(payment)
        payment.amount = payment.amount
        price = create_stripe_price(stripe_product_id=stripe_product_id, amount=payment.amount)
        session_id, payment_link = create_stripe_session(price=price)
        payment.session_id = session_id
        payment.payment_url = payment_link
        payment.save()