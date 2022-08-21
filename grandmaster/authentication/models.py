from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.core.validators import RegexValidator
from django.db import models

from datetime import timedelta
from django.utils import timezone

from utils.image_path import PathAndHash


class UserManager(BaseUserManager):
    def create_user(
            self,
            phone_number,
            password=None,
            is_active=True,
            is_admin=False,
            **kwargs
    ):
        if not phone_number:
            raise ValueError("Users must have a phone number")

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

    b24_id = models.CharField(max_length=100, null=True)  # ID
    photo = models.ImageField(upload_to=UserPathAndHash('photo'), null=True)  # PHOTO
    gender = models.CharField(max_length=100, null=True)  # HONORIFIC
    first_name = models.CharField(max_length=100, null=True)  # NAME
    last_name = models.CharField(max_length=100, null=True)  # LAST_NAME
    middle_name = models.CharField(max_length=100, null=True)  # SECOND_NAME
    birth_date = models.DateTimeField(null=True)  # BIRTHDATE
    contact_type = models.CharField(max_length=100, null=True)  # TYPE_ID
    phone_number = models.CharField(max_length=100, unique=True)  # UF_CRM_1603290188

    sport_school = models.CharField(max_length=200, null=True)  # UF_CRM_1602237440
    department = models.CharField(max_length=100, null=True)  # UF_CRM_1602237201
    trainer_name = models.CharField(max_length=100, null=True)  # UF_CRM_1568455087434
    training_place = models.CharField(max_length=200, null=True)  # UF_CRM_1602445018
    tech_qualification = models.CharField(max_length=100, null=True)  # UF_CRM_1602237683
    sport_qualification = models.CharField(max_length=100, null=True)  # UF_CRM_1602237575
    weight = models.IntegerField(null=True)  # UF_CRM_1602237818
    height = models.IntegerField(null=True)  # UF_CRM_1602237890

    region = models.CharField(max_length=200, null=True)  # UF_CRM_1628160591
    city = models.CharField(max_length=200, null=True)  # UF_CRM_1602233637
    address = models.CharField(max_length=200, null=True)  # UF_CRM_1602233739
    school = models.CharField(max_length=200, null=True)  # UF_CRM_1602234869
    med_certificate_date = models.DateTimeField(null=True)  # UF_CRM_1602237971
    insurance_policy_date = models.DateTimeField(null=True)  # UF_CRM_1602238043

    father_full_name = models.CharField(max_length=100, null=True)  # UF_CRM_1602238578
    father_birth_date = models.DateTimeField(null=True)  # UF_CRM_1602241365
    father_phone_number = models.CharField(max_length=100, null=True)  # UF_CRM_1602241669
    father_email = models.EmailField(null=True)  # UF_CRM_1602241730

    mother_full_name = models.CharField(max_length=100, null=True)  # UF_CRM_1602241765
    mother_birth_date = models.DateTimeField(null=True)  # UF_CRM_1602241804
    mother_phone_number = models.CharField(max_length=100, null=True)  # UF_CRM_1602241833
    mother_email = models.EmailField(null=True)  # UF_CRM_1602241870

    passport_or_birth_certificate = models.ImageField(upload_to=DocumentsPathAndHash('passport_or_birth_certificate'),
                                                      null=True)  # UF_CRM_1602238184
    oms_policy = models.ImageField(upload_to=DocumentsPathAndHash('oms_policy'), null=True)  # UF_CRM_1602238239
    school_ref = models.ImageField(upload_to=DocumentsPathAndHash('school_ref'), null=True)  # UF_CRM_1602238293
    insurance_policy = models.ImageField(upload_to=DocumentsPathAndHash('insurance_policy'),
                                         null=True)  # UF_CRM_1602238335
    tech_qual_diplo = models.ImageField(upload_to=DocumentsPathAndHash('tech_qual_diplo'),
                                        null=True)  # UF_CRM_1602238381
    med_certificate = models.ImageField(upload_to=DocumentsPathAndHash('med_certificate'),
                                        null=True)  # UF_CRM_1602238435
    foreign_passport = models.ImageField(upload_to=DocumentsPathAndHash('foreign_passport'),
                                         null=True)  # UF_CRM_1602238474
    inn = models.ImageField(upload_to=DocumentsPathAndHash('inn'), null=True)  # UF_CRM_CONTACT_1656319970203
    diploma = models.ImageField(upload_to=DocumentsPathAndHash('diploma'), null=True)  # UF_CRM_CONTACT_1656319776732
    snils = models.ImageField(upload_to=DocumentsPathAndHash('snils'), null=True)  # UF_CRM_CONTACT_1656320071632

    parents = models.ManyToManyField('self', related_name='children', symmetrical=False, blank=True)
    trainer = models.ForeignKey('self', related_name='students', on_delete=models.DO_NOTHING, null=True)

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
        return (bool(self.city) and
                bool(self.address) and
                bool(self.med_certificate_date) and
                bool(self.insurance_policy_date) and
                (self.med_certificate_date - timezone.now() > timedelta(days=3)) and
                (self.insurance_policy_date - timezone.now() > timedelta(days=3)) and
                self.passport_or_birth_certificate and
                self.oms_policy and
                self.insurance_policy and
                self.med_certificate and
                not any([bill.is_blocked for bill in self.bills.all()]))

    @property
    def full_name(self) -> str:
        last_name = self.last_name if self.last_name else ""
        first_name = self.first_name if self.first_name else ""
        middle_name = self.middle_name if self.middle_name else ""
        return " ".join([last_name, first_name, middle_name])

    def get_short_name(self):
        return self.phone_number

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
        return self.active


class Document(models.Model):
    user = models.ForeignKey(to=User, related_name='other_documents', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=DocumentsPathAndHash('other'))

    class Meta:
        db_table = 'documents'


class PhoneOTP(models.Model):
    phone_regex = RegexValidator(
        regex=r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}',
        message='Phone number must be entered in the format: ...',
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=12, unique=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0)
    last_modified = models.DateTimeField(auto_now=True)
    used = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.phone_number) + 'is sent' + str(self.count)

    @property
    def is_used(self):
        return self.used
