from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.utils import timezone


class Agency(models.Model):
    name = models.CharField(max_length=100, null=True)
    reg = models.CharField(max_length=20, null=True, blank=True)
    logo = models.ImageField(max_length=200, default="profile1.png", null=True, blank=True)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, phone, email, password=None):
        if not phone:
            raise ValueError('Users must have an mobile phone')

        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(phone=phone, email=email)

        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, phone, email, password):
        user = self.create_user(phone, email, password)

        user.is_superuser = True
        # user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=8, unique=True)
    email = models.EmailField(max_length=250, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    # is_admin = models.BooleanField(default=False)    
    date_joined = models.DateTimeField(default=timezone.now)
    cea_reg = models.CharField(max_length=10, blank=True, null=True)
    designation = models.CharField(max_length=50, blank=True, null=True)
    about_me = models.TextField(max_length=500, blank=True, null=True)
    profile_image = models.ImageField(null=True)
    agency = models.ForeignKey(Agency, null=True, on_delete=models.SET_NULL)
    verified = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email',]

    def __str__(self):
        return self.phone

    def get_full_name(self):
        if self.name:
            return self.name
        else:
            return self.phone

    def get_short_name(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_staff

    @property
    def is_admin(self):
        return self.is_admin

    @property
    def is_active(self):
        return self.is_active


class PhoneOTP(models.Model):
    phone = models.CharField(max_length=8, unique=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0, help_text = 'Number of otp sent')
    validated = models.BooleanField(default=False, help_text="if it is true, that means user have validate opt correctly in second API")

    def __str__(self):
        return str(self.phone) + ' is sent' + str(self.otp)
