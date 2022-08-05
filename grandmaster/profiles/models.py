from datetime import timedelta, datetime

from django.db import models
from django.contrib.auth import get_user_model

from utils.image_path import PathAndHash

User = get_user_model()


class UserProfilesPathAndHash(PathAndHash):
    def __init__(self, path):
        super().__init__('profiles/' + path)


class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='profile')
    b24_id = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    middle_name = models.CharField(max_length=100, null=True)
    birth_date = models.DateTimeField(null=True)
    trainer = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    school = models.CharField(max_length=200, null=True)
    sport_school = models.CharField(max_length=200, null=True)
    tech_qualification = models.CharField(max_length=100, null=True)
    sport_qualification = models.CharField(max_length=100, null=True)
    weight = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    med_certificate_date = models.DateTimeField(null=True)
    insurance_policy_date = models.DateTimeField(null=True)
    training_place = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=100, null=True)
    region = models.CharField(max_length=200, null=True)

    father_full_name = models.CharField(max_length=100, null=True)
    father_birth_date = models.DateTimeField(null=True)
    father_phone_number = models.CharField(max_length=100, null=True)  # TODO: change?
    father_email = models.EmailField(null=True)
    mother_full_name = models.CharField(max_length=100, null=True)
    mother_birth_date = models.DateTimeField(null=True)
    mother_phone_number = models.CharField(max_length=100, null=True)  # TODO: change?
    mother_email = models.EmailField(null=True)

    class Meta:
        db_table = 'user_profiles'

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
        return self.city and \
               self.address and \
               (self.med_certificate_date - datetime.now() > timedelta(days=3)) and \
               (self.insurance_policy_date - datetime.now() > timedelta(days=3)) and \
               False  # 3, 4 TODO: end this


class DocumentsPathAndHash(UserProfilesPathAndHash):
    def __init__(self, path):
        super().__init__('documents/' + path)


class Documents(models.Model):
    user_profile = models.OneToOneField(to=UserProfile, on_delete=models.CASCADE, related_name='documents')
    passport_or_birth_certificate = models.ImageField(upload_to=DocumentsPathAndHash('passport_or_birth_certificate'),
                                                      null=True)
    oms_policy = models.ImageField(upload_to=DocumentsPathAndHash('oms_policy'), null=True)
    school_ref = models.ImageField(upload_to=DocumentsPathAndHash('school_ref'), null=True)
    insurance_policy = models.ImageField(upload_to=DocumentsPathAndHash('insurance_policy'), null=True)
    tech_qual_diplo = models.ImageField(upload_to=DocumentsPathAndHash('tech_qual_diplo'), null=True)
    med_certificate = models.ImageField(upload_to=DocumentsPathAndHash('med_certificate'), null=True)
    foreign_passport = models.ImageField(upload_to=DocumentsPathAndHash('foreign_passport'), null=True)
    inn = models.ImageField(upload_to=DocumentsPathAndHash('inn'), null=True)
    diploma = models.ImageField(upload_to=DocumentsPathAndHash('diploma'), null=True)
    snils = models.ImageField(upload_to=DocumentsPathAndHash('snils'), null=True)
    # TODO: Add others field

    class Meta:
        db_table = 'documents'

    def __str__(self):
        return str(self.user_profile.user)
