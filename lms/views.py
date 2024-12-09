from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    get_object_or_404,
)

from drf_yasg.utils import swagger_auto_schema
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from lms.models import Course, Lesson, Subscription
from lms.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer, SubscriptionSerializer
from users.permissions import IsModerator, IsOwner
from rest_framework.response import Response
from rest_framework.views import APIView
from config.settings import EMAIL_HOST_USER
from lms.paginators import CustomPagination
from rest_framework.decorators import api_view, action
from lms.tasks import mail_update_course_info



class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        """
        Автоматическая привязка автора курса
        """
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def perform_update(self, serializer):
        updated_course = serializer.save()
        mail_update_course_info.delay(updated_course)
        updated_course.save()

    def get_permissions(self):
        """
        Права рользователей и модераторов
        """
        if self.action == "create":
            # может выполнять создание записей
            self.permission_classes = (~IsModerator,)
        elif self.action in ["update", "retrieve"]:
            # может выполнять изменение и просмотр записей
            self.permission_classes = (IsModerator | IsOwner,)
        elif self.action == "destroy":
            # для удаления записи пользователь должен быть владельцем
            self.permission_classes = (~IsModerator | IsOwner,)
        return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModerator, IsAuthenticated)

    def perform_create(self, serializer):
        """
        Автоматическая привязка автора урока
        """
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner | ~IsModerator)


class SubscriptionCreateAPIView(CreateAPIView):

    """Эндпоинт управления подпиской"""
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        # id курса, которое передал пользователь
        course_id = self.request.data.get('course')
        # данные по курсу, который запросил пользователь
        course_item = get_object_or_404(Course, pk=course_id)
        # queryset на сущность подписки фильтр по вошедшему пользователю и курсу
        subs_item = Subscription.objects.filter(course=course_item, user=user)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:# Если подписки у пользователя на этот курс нет - создаем ее
            Subscription.objects.create(course=course_item, user=user)
            message = 'Подписка добавлена'

        return Response({'message': message})# Возвращаем ответ в API


class SubscriptionListAPIView(ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer