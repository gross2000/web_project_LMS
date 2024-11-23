from django.core.management import BaseCommand
from users.models import User
from users.models import Payment
from django.utils import timezone
from django.db import models


class Command(BaseCommand):
    help = 'Команда для заполнения таблицы в БД'
    def handle(self, *args, **options):
        user = User.objects.create(email="admin@example.com")
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password("123qwerty")
        user.save()
        payment = Payment.objects.create(
            user=user,
            payment_date=timezone.now(),
            paid_course=None,
            paid_lesson=None,
            amount=100.00,
            payment_method='cash'
        )
