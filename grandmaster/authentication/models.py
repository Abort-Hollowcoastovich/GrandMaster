from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.core.validators import RegexValidator
from django.db import models

from datetime import timedelta
from django.utils import timezone

from utils.image_path import PathAndHash


class UserManager(BaseUserManager):
    def create_user(
            self,
            phone_number=None,
            password=None,
            is_active=True,
            is_admin=False,
            **kwargs
    ):

        user_obj = self.model(
            phone_number=phone_number,
            active=is_active,
            admin=is_admin,
            **kwargs
        )
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(
            self,
            phone_number,
            password=None,
            is_active=True,
            is_admin=True,
            **kwargs
    ):
        user = self.create_user(
            phone_number,
            password=password,
            is_active=is_active,
            is_admin=is_admin,
            **kwargs
        )
        return user


class UserPathAndHash(PathAndHash):
    def __init__(self, path):
        super().__init__('users/' + path)


class DocumentsPathAndHash(UserPathAndHash):
    def __init__(self, path):
        super().__init__('documents/' + path)


class User(AbstractBaseUser, PermissionsMixin):
    class Group:
        ADMINISTRATOR = "Administrator"
        MODERATOR = "Moderator"
        STUDENT = "Student"
        PARENT = "Parent"
        TRAINER = "Trainer"

    class CONTACT:
        SPORTSMAN = "CLIENT"
        TRAINER = "PARTNER"
        PARENT = "PARENT"
        MODERATOR = "MODERATOR"
        SPECIALIST = "1"

    phone_regex = RegexValidator(
        regex=r"^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}",
        message='Phone number must be entered in the format: ...',
    )

    password = models.CharField(max_length=100, null=True)
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = UserManager()

    b24_id = models.CharField(max_length=100, null=True, verbose_name='id в битриксе')  # ID
    photo = models.ImageField(upload_to=UserPathAndHash('photo'), null=True, blank=True, verbose_name='Фото')  # PHOTO
    gender = models.CharField(max_length=100, null=True, verbose_name='Пол')  # HONORIFIC
    first_name = models.CharField(max_length=100, null=True, verbose_name='Имя')  # NAME
    last_name = models.CharField(max_length=100, null=True, verbose_name='Фамилия')  # LAST_NAME
    middle_name = models.CharField(max_length=100, null=True, verbose_name='Отчество')  # SECOND_NAME
    birth_date = models.DateTimeField(null=True, verbose_name='Дата рождения')  # BIRTHDATE
    contact_type = models.CharField(max_length=100, null=True, blank=True, verbose_name='Тип контакта')  # TYPE_ID
    phone_number = models.CharField(max_length=100, unique=True, verbose_name='Номер телефона', null=True, blank=True)  # UF_CRM_1603290188

    sport_school = models.CharField(max_length=200, null=True, verbose_name='Спортивная школа')  # UF_CRM_1602237440
    department = models.CharField(max_length=100, null=True, verbose_name='Департамент')  # UF_CRM_1602237201
    trainer_name = models.CharField(max_length=100, null=True, verbose_name='ФИО тренера')  # UF_CRM_1568455087434
    training_place = models.CharField(max_length=200, null=True, verbose_name='Место тренеровок')  # UF_CRM_1602445018
    tech_qualification = models.CharField(max_length=100, null=True, verbose_name='Техническая квалификация')  # UF_CRM_1602237683
    sport_qualification = models.CharField(max_length=100, null=True, verbose_name='Спортивная квалификация')  # UF_CRM_1602237575
    weight = models.IntegerField(null=True, verbose_name='Вес')  # UF_CRM_1602237818
    height = models.IntegerField(null=True, verbose_name='Рост')  # UF_CRM_1602237890

    region = models.CharField(max_length=200, null=True, verbose_name='Регион')  # UF_CRM_1628160591
    city = models.CharField(max_length=200, null=True, verbose_name='Город')  # UF_CRM_1602233637
    address = models.CharField(max_length=200, null=True, verbose_name='Адрес')  # UF_CRM_1602233739
    school = models.CharField(max_length=200, null=True, verbose_name='Школа')  # UF_CRM_1602234869
    med_certificate_date = models.DateTimeField(null=True, verbose_name='Дата окончания медицинской справки')  # UF_CRM_1602237971
    insurance_policy_date = models.DateTimeField(null=True, verbose_name='Дата окончания страхового полиса')  # UF_CRM_1602238043

    father_full_name = models.CharField(max_length=100, null=True, verbose_name='ФИО отца')  # UF_CRM_1602238578
    father_birth_date = models.DateTimeField(null=True, verbose_name='Дата рождения отца')  # UF_CRM_1602241365
    father_phone_number = models.CharField(max_length=100, null=True, verbose_name='Телефонный номер отца')  # UF_CRM_1602241669
    father_email = models.EmailField(null=True, verbose_name='Email отца')  # UF_CRM_1602241730

    mother_full_name = models.CharField(max_length=100, null=True, verbose_name='ФИО матери')  # UF_CRM_1602241765
    mother_birth_date = models.DateTimeField(null=True, verbose_name='Дата рождения матери')  # UF_CRM_1602241804
    mother_phone_number = models.CharField(max_length=100, null=True, verbose_name='Номер телефона матери')  # UF_CRM_1602241833
    mother_email = models.EmailField(null=True, verbose_name='Email матери')  # UF_CRM_1602241870

    passport_or_birth_certificate = models.FileField(upload_to=DocumentsPathAndHash('passport_or_birth_certificate'),
                                                     null=True, verbose_name='Паспорт или свидетельство о рождении')  # UF_CRM_1602238184
    oms_policy = models.FileField(upload_to=DocumentsPathAndHash('oms_policy'), null=True, verbose_name='Полис')  # UF_CRM_1602238239
    school_ref = models.FileField(upload_to=DocumentsPathAndHash('school_ref'), null=True, verbose_name='Справка со школы')  # UF_CRM_1602238293
    insurance_policy = models.FileField(upload_to=DocumentsPathAndHash('insurance_policy'), verbose_name='Страховой полис',
                                        null=True)  # UF_CRM_1602238335
    tech_qual_diplo = models.FileField(upload_to=DocumentsPathAndHash('tech_qual_diplo'), verbose_name='Диплом о технической квалификации',
                                       null=True)  # UF_CRM_1602238381
    med_certificate = models.FileField(upload_to=DocumentsPathAndHash('med_certificate'), verbose_name='Медицинская справка',
                                       null=True)  # UF_CRM_1602238435
    foreign_passport = models.FileField(upload_to=DocumentsPathAndHash('foreign_passport'), verbose_name='Загран. паспорт',
                                        null=True)  # UF_CRM_1602238474
    inn = models.FileField(upload_to=DocumentsPathAndHash('inn'), null=True, verbose_name='ИНН')  # UF_CRM_CONTACT_1656319970203
    diploma = models.FileField(upload_to=DocumentsPathAndHash('diploma'), null=True, verbose_name='Диплом')  # UF_CRM_CONTACT_1656319776732
    snils = models.FileField(upload_to=DocumentsPathAndHash('snils'), null=True, verbose_name='Снилс')  # UF_CRM_CONTACT_1656320071632

    parents = models.ManyToManyField('self', related_name='children', symmetrical=False, blank=True, verbose_name='Родители')
    trainer = models.ForeignKey('self', related_name='students', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Тренер')  # UF_CRM_1568455087434

    def __contains__(self, group_name):
        # Example: User.Group.PARENT in user_object
        group, created = Group.objects.get_or_create(name=group_name)
        return group in self.groups.all()

    def add_group(self, group_name):
        group, created = Group.objects.get_or_create(name=group_name)
        self.groups.add(group)

    # Допуск. Эти поля участвуют в вычислекнии Статуса Допущен/Не допущен.
    # 1. Поле не должно быть пустым.
    # (город, адрес)
    # 2. Эти даты не должны быть меньше, чем Текущая дата + 3 дня.
    # (медицинская справка дата, страховой полис дата)
    # 3. Файлы должны быть загружены.
    # (фотография, паспорт/свидетельство о рождении, полис ОМС, страховой полис, медицинская справка)
    # 4. Не должно быть неоплаченных счетов с "Датой оплаты" текущая дата + 3 дня
    @property
    def is_admitted(self) -> bool:
        return (bool(self.photo) and
                bool(self.first_name) and
                bool(self.last_name) and
                bool(self.middle_name) and
                bool(self.birth_date) and
                bool(self.trainer_name) and
                bool(self.city) and
                bool(self.address) and
                bool(self.weight) and
                bool(self.height) and
                bool(self.med_certificate_date) and
                bool(self.insurance_policy_date) and
                (self.med_certificate_date - timezone.now() > timedelta(days=3)) and
                (self.insurance_policy_date - timezone.now() > timedelta(days=3)) and
                self.passport_or_birth_certificate and
                bool(self.oms_policy) and
                bool(self.insurance_policy) and
                bool(self.med_certificate) and
                bool(self.training_place) and
                bool(self.phone_number) and
                bool(self.region) and
                not any([bill.is_blocked for bill in self.bills.all()]))

    @property
    def full_name(self) -> str:
        last_name = self.last_name if self.last_name else ""
        first_name = self.first_name if self.first_name else ""
        middle_name = self.middle_name if self.middle_name else ""
        return " ".join([last_name, first_name, middle_name])

    def get_short_name(self):
        return f'{self.phone_number} {self.full_name}'

    def __str__(self) -> str:
        return self.full_name

    @property
    def is_staff(self):
        return self.admin

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_superuser(self):
        return self.admin

    @property
    def is_active(self):
        if self.contact_type:
            return self.active and bool(self.contact_type.strip())
        return False

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Document(models.Model):
    user = models.ForeignKey(to=User, related_name='other_documents', on_delete=models.CASCADE, verbose_name='Пользователь')
    image = models.FileField(upload_to=DocumentsPathAndHash('other'), verbose_name='Документ')

    class Meta:
        db_table = 'documents'
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


class PhoneOTP(models.Model):
    phone_regex = RegexValidator(
        regex=r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}',
        message='Phone number must be entered in the format: ...',
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=12, unique=True, verbose_name='Телефонный номер')
    otp = models.CharField(max_length=9, blank=True, null=True, verbose_name='Код')
    count = models.IntegerField(default=0, verbose_name='Счетчик активаций')
    last_modified = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')
    used = models.BooleanField(default=False, verbose_name='Использован')

    def __str__(self) -> str:
        return str(self.phone_number) + 'is sent' + str(self.count)

    @property
    def is_used(self):
        return self.used

    class Meta:
        verbose_name = 'Телефонный код'
        verbose_name_plural = 'Телефонные коды'

