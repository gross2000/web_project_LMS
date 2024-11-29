from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from courses.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="testdrive@gmail.com", password='0204')
        self.course = Course.objects.create(title="Java", user=self.user)
        self.lesson = Lesson.objects.create(title="Java", courses=self.course, user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('courses:lessons_details', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), self.lesson.title
        )

    def test_lesson_create(self):
        user2 = User.objects.create(email='testdrive2@mail.ru')
        course2 = Course.objects.create(title='Python', user=user2)
        url = reverse('courses:lessons_create')
        data = {
            'title': 'Python',
            'courses': course2.pk,
            'user': user2.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.count(), 2
        )

    def test_lesson_update(self):
        url = reverse('courses:lessons_update', args=(self.lesson.pk,))
        data = {
            'title': 'Python - начало',
        }
        response = self.client.patch(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), 'Python - начало'
        )

    def test_lesson_delete(self):
        url = reverse('courses:lessons_delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.count(), 0
        )

    def test_lesson_list(self):
        url = reverse('courses:lessons_list')
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "title": "Java",
                    "image": None,
                    "description": None,
                    "link": None,
                    "courses": self.course.pk,
                    "user": self.user.pk
                }
            ]
        }

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )


class SubscriptionTastCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="testdrive@gmail.com", password='0204')
        self.course = Course.objects.create(title="Java", user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        url = reverse('courses:subscription_create')
        data = {
            'course': self.course.pk,
        }
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            Subscription.objects.count(), 1
        )
        self.assertEqual(
            data, {'message': 'Подписка создана'}
        )

    def test_subscription_delete(self):
        url = reverse('courses:subscription_create')
        data = {
            'course': self.course.pk,
        }
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            Subscription.objects.count(), 0
        )
        self.assertEqual(
            data, {'message': 'Подписка удалена'}
        )