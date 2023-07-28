from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Users must have a phone number')

        user = self.model(phone_number=phone_number, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        user = self.create_user(phone_number, password=password, **extra_fields)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    class Sex(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'

    name = models.CharField(max_length=150, blank=True, null=True)
    sex = models.CharField(max_length=1, choices=Sex.choices, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    phone_number = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(regex='9(1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}')]  # Iran's mobile numbers' regex
    )
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        if self.name:
            return self.name
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
