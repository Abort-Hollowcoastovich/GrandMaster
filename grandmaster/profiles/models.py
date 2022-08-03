from django.db import models
from django.contrib.auth import get_user_model

from utils.image_path import PathAndHash

User = get_user_model()


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
