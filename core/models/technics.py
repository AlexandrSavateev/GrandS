import json

from django.core.validators import MinValueValidator
from django.db import models
from user.models import Driver, Dispatcher
# from mptt.models import MPTTModel, TreeForeignKey


# class Category(MPTTModel):
#     parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
#     title = models.CharField('Тип техники', max_length=50, unique=True)
#     price = models.FloatField('Стоимость в час', default=0.0,
#                               help_text='Стоимость по умолчанию для техники данной категории')
#
#     # Sortable property
#     order = models.PositiveIntegerField(verbose_name='Порядок сортировки', default=0)
#
#     def __str__(self):
#         return self.title
#
#     class MPTTMeta:
#         order_insertion_by = ('order', 'title')

class TechnicsCategory(models.Model):
    title = models.CharField('Категория техники', max_length=50, unique=True)
    is_special = models.BooleanField('Является спецтехникой', default=True)

    class Meta:
        verbose_name = 'Категория техники'
        verbose_name_plural = 'Категории техники'

    def __str__(self):
        return self.title


class TechnicsType(models.Model):
    title = models.CharField(
        'Тип техники',
        max_length=50, unique=True
    )
    category = models.ForeignKey(
        TechnicsCategory,
        related_name='types',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Тип техники'
        verbose_name_plural = 'Типы техники'

    def __str__(self):
        return self.title


class TechnicsSubTypeBase(models.Model):
    # Characteristics
    weight_from = models.DecimalField(
        'Масса от, т',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    weight_to = models.DecimalField(
        'Масса до, т',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    bucket_capacity_from = models.DecimalField(
        'Объем ковша от, м3',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    bucket_capacity_to = models.DecimalField(
        'Объем ковша до, м3',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    digging_depth_from = models.DecimalField(
        'Глубина копания от, м',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    digging_depth_to = models.DecimalField(
        'Глубина копания до, м',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    drilling_depth_from = models.DecimalField(
        'Глубина бурения от, м',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    drilling_depth_to = models.DecimalField(
        'Глубина бурения до, м',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    screw_diameter_from = models.PositiveSmallIntegerField(
        'Диаметр шнека от, мм',
        null=True, blank=True
    )
    screw_diameter_to = models.PositiveSmallIntegerField(
        'Диаметр шнека до, мм',
        null=True, blank=True
    )
    load_capacity_from = models.DecimalField(
        'Грузоподъемность от, т',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    load_capacity_to = models.DecimalField(
        'Грузоподъемность до, т',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    lift_height_from = models.DecimalField(
        'Высота подъема от, м',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    lift_height_to = models.DecimalField(
        'Высота подъема до, м',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    break_force_from = models.PositiveSmallIntegerField(
        'Вырывное усилие от, кг',
        null=True, blank=True
    )
    break_force_to = models.PositiveSmallIntegerField(
        'Вырывное усилие до, кг',
        null=True, blank=True
    )
    main_boom_length_from = models.DecimalField(
        'Длина главной стрелы от, м',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    main_boom_length_to = models.DecimalField(
        'Длина главной стрелы до, м',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    boom_length_with_trunk_from = models.DecimalField(
        'Длина стрелы с гуськом от, м',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    boom_length_with_trunk_to = models.DecimalField(
        'Длина стрелы с гуськом до, м',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    work_height_from = models.DecimalField(
        'Рабочая высота от, м',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    work_height_to = models.DecimalField(
        'Рабочая высота до, м',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    pumping_capacity_from = models.DecimalField(
        'Объем откачки от, м3',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    pumping_capacity_to = models.DecimalField(
        'Объем откачки до, м3',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    body_capacity_from = models.DecimalField(
        'Объем кузова от, м3',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    body_capacity_to = models.DecimalField(
        'Объем кузова до, м3',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    chassis_load_capacity_from = models.DecimalField(
        'Грузоподъемность шасси от, т',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    chassis_load_capacity_to = models.DecimalField(
        'Грузоподъемность шасси до, т',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    manipulator_lifting_capacity_from = models.DecimalField(
        'Грузоподъемность манипулятора от, т',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    manipulator_lifting_capacity_to = models.DecimalField(
        'Грузоподъемность манипулятора до, т',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    max_blade_length_from = models.DecimalField(
        'Мах длина грейдерного отвала от, м',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    max_blade_length_to = models.DecimalField(
        'Мах длина грейдерного отвала до, м',
        max_digits=5, decimal_places=3, null=True, blank=True
    )
    operation_weight_from = models.PositiveSmallIntegerField(
        'Эксплуатационная масса от, т', null=True, blank=True
    )
    operation_weight_to = models.PositiveSmallIntegerField(
        'Эксплуатационная масса до, т',
        null=True, blank=True
    )
    drum_width_from = models.PositiveSmallIntegerField(
        'Ширина барабана от, мм',
        null=True, blank=True
    )
    drum_width_to = models.PositiveSmallIntegerField(
        'Ширина барабана до, мм',
        null=True, blank=True
    )

    class Meta:
        abstract = True


class TechnicsSubType(TechnicsSubTypeBase):
    title = models.CharField(
        'Наименование',
        max_length=50, null=True, blank=True, unique=True
    )
    tech_type = models.ForeignKey(
        TechnicsType,
        on_delete=models.CASCADE, related_name='subtypes'
    )
    price = models.DecimalField(
        'Стоимость в м/ч',
        max_digits=10, decimal_places=3, default=0
    )
    min_time = models.PositiveSmallIntegerField(
        'Миним. время',
        default=4,
        help_text='Минимальное время аренды техники',
        validators=[MinValueValidator(4)]
    )

    class Meta:
        verbose_name = 'Подтип техники'
        verbose_name_plural = 'Подтипы техники'

    def __str__(self):
        return str(self.tech_type)


def auto_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/Technics/<category>/<filename>
    return 'Technics/{0}/{1}'.format(instance.category, filename)


class Auto(models.Model):
    subtype = models.ForeignKey(
        TechnicsSubType,
        related_name='autos',
        on_delete=models.PROTECT,
    )
    driver = models.ForeignKey(
        Driver,
        null=True,
        blank=True,
        related_name='autos',
        on_delete=models.SET_NULL,
    )
    dispatcher = models.ForeignKey(
        Dispatcher,
        related_name='autos',
        on_delete=models.CASCADE,
    )

    brand = models.CharField('Марка', max_length=20)
    model = models.CharField('Модель', max_length=20)
    number = models.CharField(
        'Регистр. номер',
        max_length=9,
        blank=False
    )
    year = models.CharField(
        'Год выпуска',
        blank=True,
        null=True,
        max_length=4)
    image = models.ImageField(
        max_length=255,
        blank=True,
        null=True,
        upload_to=auto_image_path
    )
    description = models.CharField(
        'Описание',
        blank=True,
        null=True,
        max_length=255
    )

    # Parking place
    parking_latitude = models.DecimalField(
        'Координаты стоянки (широта)',
        max_digits=9,
        decimal_places=6
    )
    parking_longitude = models.DecimalField(
        'Координаты стоянки (долгота)',
        max_digits=9,
        decimal_places=6
    )
    parking_description = models.CharField(
        'Описание стоянки',
        blank=True,
        null=True,
        max_length=250
    )

    # weather_restrictions = models.ForeignKey(
    #     Weather,
    #     on_delete=models.SET_NULL, null=True, blank=True
    # )
    road_restriction = models.BooleanField(
        'Дорожные ограничения',
        default=False
    )
    relocation = models.BooleanField(
        'Требуется перебазирование',
        default=False
    )

    is_active = models.BooleanField(
        'Активен',
        default=True
    )

    extra_rating = models.DecimalField(
        default=0,
        max_digits=2,
        decimal_places=1
    )

    def __str__(self):
        return '{} {}'.format(self.model, self.number)

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
