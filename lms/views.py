from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer
from users.permissions import IsModerator, IsOwner
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from config.settings import EMAIL_HOST_USER
from lms.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()

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