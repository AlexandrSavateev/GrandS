from django.db import models
from django.contrib.auth import get_user_model
from .technics import Auto, TechnicsType, TechnicsSubType
from user.models import User, Dispatcher

UserModel = get_user_model()


class Order(models.Model):
    client = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=False,
        related_name='client_orders'
    )
    started_at = models.DateTimeField("Начало работ")
    ended_at = models.DateTimeField("Окончание работ")
    description = models.TextField(
        "Комментарии",
        null=True, blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Время обновления'
    )

    providers = models.ManyToManyField(
        Dispatcher,
        blank=True,
        related_name='orders'
    )

    # price = models.FloatField("Стоимость работ", default=0)
    # price_add = models.FloatField("Стоимость продления", null=True, blank=True)
    is_confirm = models.BooleanField("Подтвержден", default=False)
    is_complete = models.BooleanField("Укомплектован", default=False)
    is_paid = models.BooleanField("Оплачено", default=False)
    transaction_id = models.CharField('Номер транзакции', default='', max_length=255)
    is_closed = models.BooleanField("Закрыт", default=False)

    def __str__(self):
        return "Заказ № {} клиент {}".format(self.id, self.client)

    # def check_order(self):
    #     technics = Technique.objects.filter(order=self)
    #     for tech in technics:
    #         if tech.count < len(UnitTech.objects.filter(technique__catalog=tech.catalog, technique__order=self)):
    #             return
    #     self.is_complete = True
    #     self.save()
    #     # рассчитать стоимость
    #     self.calc_order()
    #
    # def calc_order(self):
    #     total_price=0
    #     # рассчет времени
    #     time = self.ended_at - self.started_at
    #     time_hours = time.days*8 + round(time.seconds/3600)
    #     # выбор техники из заказа и рассчет стоимости
    #     technics = Technique.objects.filter(order=self)
    #     for tech in technics:
    #         units = UnitTech.objects.filter(technique__catalog=tech.catalog, technique__order=self)
    #         for unit in units:
    #             total_price = total_price + time_hours*tech.catalog.price
    #     self.price = total_price
    #     self.save()
    #     return self.price

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


def order_images_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/Orders/<order_id>/<filename>
    return 'Orders/{0}/Images/{1}'.format(instance.order.id, filename)


class OrderImage(models.Model):
    image = models.ImageField(
        max_length=255,
        upload_to=order_images_path
    )
    description = models.CharField(
        max_length=255, null=True, blank=True
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='images'
    )


class OrderPoint(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name='Заказ',
        on_delete=models.CASCADE,
        related_name='points'
    )
    latitude = models.DecimalField(
        'Широта',
        max_digits=9, decimal_places=6
    )
    longitude = models.DecimalField(
        'Долгота',
        max_digits=9, decimal_places=6
    )
    description = models.CharField(
        'Описание',
        blank=True, null=True, max_length=250
    )

    def __str__(self):
        return "Точка {}; {}".format(self.latitude, self.longitude)

    class Meta:
        verbose_name = 'Точка'
        verbose_name_plural = 'Точки'


class OrderTechnics(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name='Заказ',
        on_delete=models.CASCADE,
        related_name='technics'
    )
    tech_type = models.ForeignKey(
        TechnicsType,
        verbose_name='Тип техники',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='order_technics'
    )
    subtypes = models.ManyToManyField(
        TechnicsSubType,
        blank=True,
        verbose_name='Подтипы техники')
    quantity = models.SmallIntegerField('Количество', default=1)

    def __str__(self):
        return "Вид техники {}, кол-во {}".format(self.tech_type, self.quantity)

    class Meta:
        verbose_name = 'Вид техники (предзаказ)'
        verbose_name_plural = 'Виды техники (предзаказ)'


class OrderUnitTech(models.Model):
    technics = models.ForeignKey(
        OrderTechnics,
        on_delete=models.CASCADE,
        related_name='autos'
    )
    auto = models.ForeignKey(
        Auto,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return "Единица техники {}".format(self.auto)

    class Meta:
        verbose_name = 'Единица техники заказа'
        verbose_name_plural = 'Единицы техники заказа'


class OrderProlongation(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='prolongations')
    hours = models.PositiveSmallIntegerField('Время продления')
    auto = models.OneToOneField(
        Auto,
        on_delete=models.SET_NULL,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Время обновления'
    )

    def __str__(self):
        return "Продление техники {}".format(self.auto)

    class Meta:
        verbose_name = 'Продление техники'
        verbose_name_plural = 'Продление техники'


class OrderRequestToDispatcher(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='dispatcher_requests'
    )
    autos = models.ManyToManyField(Auto)
    time_from = models.DateTimeField('Время активации')
    is_closed = models.BooleanField('Закрыт', default=True)

    def __str__(self):
        return "Запрос диспетчеру {}, заказ {}".format(self.id, self.order_id)

    class Meta:
        verbose_name = 'Запрос диспетчеру'
        verbose_name_plural = 'Запросы диспетчеру'
