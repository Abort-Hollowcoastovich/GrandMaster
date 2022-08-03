from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator

from utils.image_path import PathAndHash


class UserManager(BaseUserManager):
    def create_user(
            self,
            phone,
            password=None,
            is_active=True,
            is_admin=False,
            **kwargs
    ):
        if not phone:
            raise ValueError("Users must have a phone number")

        user_obj = self.model(
            phone=phone,
            active=is_active,
            admin=is_admin,
            **kwargs
        )
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(
            self,
            phone,
            password=None,
            is_active=True,
            is_admin=True,
            **kwargs
    ):
        user = self.create_user(
            phone,
            password=password,
            is_active=is_active,
            is_admin=is_admin,
            **kwargs
        )
        return user


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        STUDENT = "ST"
        PARENT = "PR"
        TRAINER = "TR"
        MODERATOR = "MD"
        ADMINISTRATOR = "AD"

    phone_regex = RegexValidator(
        regex=r"^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}",
        message='Phone number must be entered in the format: ...',
    )

    role = models.CharField(max_length=2, choices=Role.choices, null=True)
    parents = models.ManyToManyField('self', symmetrical=False, related_name='children')
    # trainer = models.ManyToManyField('self', related_name='students') TODO: manytomany or foreign key

    full_name = models.CharField(max_length=100, null=True)
    phone = models.CharField(
        validators=[phone_regex], max_length=12, unique=True)
    password = models.CharField(max_length=100, null=True)

    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone

    def get_full_name(self):
        return self.full_name + self.phone

    def has_perm(self, perm, obj=None):
        return self.admin

    def has_module_perms(self, app_label):
        return self.admin

    @property
    def is_staff(self):
        return self.admin

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_superuser(self):
        return self.superuser

    @property
    def is_active(self):
        return self.active


class PhoneOTP(models.Model):
    phone_regex = RegexValidator(
        regex=r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}',
        message='Phone number must be entered in the format: ...',
    )
    phone = models.CharField(validators=[phone_regex], max_length=12, unique=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0)
    last_modified = models.DateTimeField(auto_now=True)
    used = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.phone) + 'is sent' + str(self.count)

    @property
    def is_used(self):
        return self.used


class UserPathAndHash(PathAndHash):
    def __init__(self, path):
        super().__init__('users/' + path)


class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='profile')
    b24_id = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    birth_date = models.DateTimeField()
    # trainer = None TODO: ?
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    school = models.CharField(max_length=200)
    sport_school = models.CharField(max_length=200)
    tech_qualification = models.CharField(max_length=100)
    sport_qualification = models.CharField(max_length=100)
    weight = models.IntegerField()
    height = models.IntegerField()
    med_certificate_date = models.DateTimeField()
    insurance_policy_date = models.DateTimeField()
    passport_or_birth_certificate = models.ImageField(upload_to=UserPathAndHash('passport_or_birth_certificate'))
    oms_policy = models.ImageField(upload_to=UserPathAndHash('oms_policy'))
    school_ref = models.ImageField(upload_to=UserPathAndHash('school_ref'))
    insurance_policy = models.ImageField(upload_to=UserPathAndHash('insurance_policy'))
    tech_qual_diplo = models.ImageField(upload_to=UserPathAndHash('tech_qual_diplo'))
    med_certificate = models.ImageField(upload_to=UserPathAndHash('med_certificate'))
    foreign_passport = models.ImageField(upload_to=UserPathAndHash('foreign_passport'))
    father_full_name = models.CharField(max_length=100)
    father_birth_date = models.DateTimeField()
    father_phone_number = models.CharField(max_length=100)  # TODO: change?
    father_email = models.EmailField()
    mother_full_name = models.CharField(max_length=100)
    mother_birth_date = models.DateTimeField()
    mother_phone_number = models.CharField(max_length=100)  # TODO: change?
    mother_email = models.EmailField()
    training_place = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=100)
    region = models.CharField(max_length=200)
    diploma = models.ImageField(upload_to=UserPathAndHash('diploma'))
    inn = models.ImageField(upload_to=UserPathAndHash('inn'))
    snils = models.ImageField(upload_to=UserPathAndHash('snils'))

    class Meta:
        db_table = 'user_profiles'


class DocumentPathAndHash(PathAndHash):
    def __init__(self, path):
        super().__init__('documents/' + path)


class Document(models.Model):
    user_profile = models.ForeignKey(to=UserProfile, related_name='documents', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to=DocumentPathAndHash('image'))

    class Meta:
        db_table = 'documents'
