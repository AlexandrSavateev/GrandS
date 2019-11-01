from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.core.mail import send_mail


def create_address():
    """Create new address object for default"""
    address = Address.objects.create()
    return address.id


def create_organization():
    """Create new organization object for default"""
    org = Organization.objects.create()
    return org.id


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not phone:
            raise ValueError('Номер телефона должен присутствовать!')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone,  password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


def user_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/Users/<phone>/<filename>
    return 'Users/{0}/{1}'.format(instance.phone[1:], filename)


class User(AbstractBaseUser, PermissionsMixin):
        # AbstractBaseUser for full customizing User model(Egor Chernik)
        # Used if extremely necessary only(Egor Chernik)
    phone = models.CharField('Телефон', max_length=13, unique=True)
    email = models.EmailField('Email', blank=True, null=True, unique=True)
    first_name = models.CharField('Имя', max_length=30, null=True, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, null=True, blank=True)
    patronymic = models.CharField('Отчество', max_length=255, null=True, blank=True)
    image = models.ImageField(max_length=255, null=True, blank=True, upload_to=user_image_path)
        # avatar. Why not set the default pic?(Egor Chernik)
    date_joined = models.DateTimeField('Дата регистрации', default=timezone.now)
    date_modified = models.DateTimeField('Дата изменения', auto_now=True)
    is_staff = models.BooleanField('Является администратором', default=False)
        # field for access Django Admin only(Egor Chernik)
    is_active = models.BooleanField('Активный пользователь', default=True)
        # field for "deleting" (hiding) users(Egor Chernik)
        # if you want delete user it is better change his status is_active to False(Egor Chernik)
    user_type = models.IntegerField('Привелегии', null=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'phone'
        # required basefield. Used when instead username you want to use smth else(Egor Chernik)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return '{} {}'.format(self.phone, self.get_full_name())

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """ Return the first_name plus the last_name,
            with a space between. Ivanov Ivan Ivanovich, e.g."""
        full_name = ''
        if self.last_name:
            full_name += self.last_name[:1].upper()+self.last_name[1:]
            if self.first_name:
                full_name += self.first_name[:1].upper()+self.first_name[1:]
                if self.patronymic:
                    full_name += self.patronymic[:1].upper()+self.patronymic[1:]
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user. Ivanov I.I. ,e.g."""
        short_name = ''
        if self.last_name:
            short_name += self.last_name[:1].upper()+self.last_name[1:]
                # capitalize() doesn't work here.
                # CharField has no such method (Egor Chernik)
            if self.first_name:
                short_name += ' ' + self.first_name[:1].upper() + '.'
                if self.patronymic:
                    short_name += ' ' + self.patronymic[:1].upper() + '.'
        return short_name.strip()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Address(models.Model):
    COUNTRY_BELARUS = 1

    TYPE_COUNTRY = (
        (COUNTRY_BELARUS, 'РБ'),
    )

    country = models.PositiveSmallIntegerField('Страна', choices=TYPE_COUNTRY, default=COUNTRY_BELARUS)
    city = models.CharField('Населеннный пункт', max_length=50, default='unknown')
    street = models.CharField('Улица', max_length=50, null=True)
    house = models.CharField('Дом', max_length=5, null=True)
    housing = models.CharField('Корпус', max_length=2, null=True, blank=True)
    office = models.CharField('Офис/квартира', max_length=5, null=True)
    description = models.CharField('Доп. информация', max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        res = ''
        if self.city: res += 'г.' + self.city # And if it is village or smth else?(Egor Chernik)
        if self.street: res += ' ул.' + self.street
        if self.house: res += ' д.' + self.house
        if self.housing: res += ' к.' + self.housing
        if self.office: res += ' оф./кв.' + self.office
        return res


def certificate_image_path(instance, filename):
    user_folder = 'default_folder'
    if hasattr(instance, 'clientlegal'):
        user_folder = instance.clientlegal.phone[1:]
    elif hasattr(instance, 'dispatcher'):
        user_folder = instance.dispatcher.phone[1:]
    # file will be uploaded to MEDIA_ROOT/Users/<phone>/<filename>
    return 'Users/{0}/{1}'.format(user_folder, filename)


class Organization(models.Model):
    name = models.CharField('Наименование', max_length=50, default='unknown')
    unp = models.CharField('УНП', max_length=10, null=True)
    address = models.OneToOneField(Address, related_name='org_address', on_delete=models.PROTECT, default=create_address)
    post_address = models.OneToOneField(Address, related_name='post_address', on_delete=models.PROTECT, default=create_address)
    # Платежные реквизиты
    bank = models.CharField('Банк', max_length=50, null=True)
    bank_department = models.CharField('Отделение банка', max_length=255, null=True)
    bank_address = models.CharField('Адрес банка', max_length=255, null=True)
    bank_bik = models.CharField('БИК банка', max_length=15, null=True)
    contact_org = models.CharField('Контакты организации', max_length=255, null=True)
    iban = models.CharField('p/c в формате IBAN',max_length=28, null=True)
    first_person = models.CharField('Руководитель', max_length=50, null=True)
    acting_on = models.CharField('Действующий на основании', max_length=50, null=True)
    accountant = models.CharField('Бухгалтер', max_length=50, null=True)
    contact_person = models.CharField('Контактное лицо', max_length=50, null=True)
    add_contact = models.CharField('Доп. контакты', max_length=255, null=True)
    certificate = models.ImageField('Свидетельство о регистрации', null=True, blank=False, upload_to=certificate_image_path)

    class Meta:
        verbose_name = 'Юридическое лицо'
        verbose_name_plural = 'Юридические лица'

    def get_address(self):
        return str(self.address)

    def get_post_address(self):
        return str(self.post_address)

    def __str__(self):
        return self.name


class ClientPrivate(User):
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    person_id = models.CharField('Личный номер', max_length=50, blank=True, null=True)

    #person_doc_series = models.CharField('Серия документа', max_length=2, blank=True, null=True)
    #person_doc_number = models.CharField('Номер документа', max_length=7, blank=True, null=True)
    #person_authority = models.CharField('Орган, выдавший документ', max_length=50, blank=True, null=True)
    #person_doc_issued_date = models.DateField('Дата выдачи', null=True, blank=True)

    address = models.OneToOneField(Address, on_delete=models.PROTECT, related_name='client', default=create_address)

    class Meta:
        verbose_name = 'Клиент (физ. лицо)'
        verbose_name_plural = 'Клиенты (физ. лица)'

    def get_address(self):
        return str(self.address)


class ClientLegal(User):
    organization = models.OneToOneField(Organization, on_delete=models.PROTECT, default=create_organization)

    class Meta:
        verbose_name = 'Клиент (юр. лицо)'
        verbose_name_plural = 'Клиенты (юр. лица)'

    def get_address(self):
        return self.organization.get_address()

    def get_post_address(self):
        return self.organization.get_post_address()

# contractor, transport's owner(Egor Chernik)
class Dispatcher(User):
    organization = models.OneToOneField(Organization, on_delete=models.PROTECT, default=create_organization)

    class Meta:
        verbose_name = 'Диспетчер'
        verbose_name_plural = 'Диспетчеры'

    def get_address(self):
        return self.organization.get_address()

    def get_post_address(self):
        return self.organization.get_post_address()


class Driver(models.Model):
    ST_WORK_READY = 1
    ST_ORDER_ACCEPT = 2
    ST_CAME_PLACE = 3
    ST_WENT_NEXT_POINT = 4
    ST_COMPLETE = 5
    ST_RETURN_BASE = 6

    DRIVER_STATUS = (
        (ST_WORK_READY, 'готов к работе'),
        (ST_ORDER_ACCEPT, 'заказ принят'),
        (ST_CAME_PLACE, 'приехал на место выполнения работы/место загрузки'),
        (ST_WENT_NEXT_POINT, 'выехал на следующую точку'),
        (ST_COMPLETE, 'работа завершена'),
        (ST_RETURN_BASE, 'вернулся на базу'),
    )
    status = models.PositiveSmallIntegerField('Статус', choices=DRIVER_STATUS, default=ST_WORK_READY)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dispatcher = models.ForeignKey(Dispatcher, on_delete=models.CASCADE, related_name='driver_dispatcher')
    extra_rating = models.DecimalField(default=0, max_digits=3, decimal_places=2)

    class Meta:
        verbose_name = 'Водитель'
        verbose_name_plural = 'Водители'

    def __str__(self):
        return str(self.user)
