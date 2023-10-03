from django.db import models
from django.db.models import Model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save


class CustomUserManager(BaseUserManager):

    def create_user(self, user_code, password=None, **other_fields):

        if not user_code:
            raise ValueError(_('User code must be set'))
        user_code = user_code.strip()
        user = self.model(user_code=user_code, **other_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_code, password=None, **other_fields):

        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser',True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(_('is_staff field must be True'))
        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('is_superuser field must be True'))

        return self.create_user(user_code, password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    
    user_code = models.CharField(max_length=14, unique=True)
    is_active = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'user_code'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.user_code


class StudentProfile(Model):

    PERIOD = (
        ('M', 'morning'),
        ('V', 'vespertine'),
        ('N', 'night')
        )

    name = models.CharField(max_length=64)
    address = models.CharField(max_length=128)
    diploma_issued = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    course = models.CharField(max_length=64)
    period = models.CharField(choices=PERIOD, max_length=1, blank=False, null=False, default='M')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.email


class TeacherProfile(Model):
    subject = models.CharField(max_length=64)
    name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.email


def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_teacher:
            TeacherProfile.objects.create(user=instance)
        else:
            StudentProfile.objects.create(user=instance)

post_save.connect(create_profile, sender=User)