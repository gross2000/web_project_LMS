from django.db import models
from config.settings import AUTH_USER_MODEL


NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="введите название курса",
    )
    preview = models.ImageField(
        upload_to="lms/preview/course", verbose_name="Превью", blank=True, null=True
    )
    description = models.TextField(
        verbose_name="Описание курса", help_text="укажите описание курса"
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Создатель курса",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(
        max_length=50, verbose_name="Название урока", help_text="укажите название урока"
    )
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, verbose_name="Курс", blank=True, null=True, related_name='lessons'
    )
    description = models.TextField(
        verbose_name="Описание урока", help_text="укажите описание урока"
    )
    preview = models.ImageField(
        upload_to="lms/preview/lesson", verbose_name="Превью", blank=True, null=True
    )
    link_to_video = models.CharField(
        max_length=200,
        verbose_name="Ссылка на видео",
        blank=True,
        null=True,
        help_text="укажите ссылку на видео материал",
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Создатель урока",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    sign_up = models.BooleanField(default=False, verbose_name="Подписка")

    def __str__(self):
        return f"{self.user}: ({self.course})"


    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'