from django.db import models
from .technics import Auto, Driver


class Review(models.Model):
    """
       Отзыв с оценкой
    """
    title = models.CharField(
        max_length=100,
        verbose_name='Заголовок'
    )
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    value = models.IntegerField(
        choices=RATING_CHOICES,
        verbose_name='Оценка',
        default=5
    )
    body = models.TextField(
        verbose_name='Описание'
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликован'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Время обновления'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return '{} Оценка: {}'.format(self.title, self.value)


class AutoReview(Review):
    """
    Отзыв с оценкой по автомобилю
    """
    auto = models.ForeignKey(
        Auto,
        verbose_name='Автомобиль',
        related_name='reviews',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Отзыв по автомобилю'
        verbose_name_plural = 'Отзывы по автомобилям'


def auto_review_images_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/Orders/<order_id>/<filename>
    parent_path = instance.auto._meta.get_field('image').upload_to(instance.auto, '')
    return parent_path + 'Reviews/{0}/{1}'.format(instance.review.name, filename)


class AutoReviewImage(models.Model):
    image = models.ImageField(
        max_length=255,
        upload_to=auto_review_images_path
    )
    description = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    review = models.ForeignKey(
        AutoReview,
        related_name='images',
        on_delete=models.CASCADE,
    )


class DriverReview(Review):
    """
    Отзыв с оценкой по водителю
    """

    driver = models.ForeignKey(
        Driver,
        verbose_name='Водитель',
        related_name='reviews',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Отзыв по водителю'
        verbose_name_plural = 'Отзывы по водителям'


def driver_review_images_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/Orders/<order_id>/<filename>
    parent_path = instance.driver._meta.get_field('image').upload_to(instance.driver, '')
    return parent_path + 'Reviews/{0}/{1}'.format(instance.review.name, filename)


class DriverReviewImage(models.Model):
    image = models.ImageField(
        max_length=255,
        upload_to=driver_review_images_path
    )
    description = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    review = models.ForeignKey(
        DriverReview,
        related_name='images',
        on_delete=models.CASCADE,
    )
