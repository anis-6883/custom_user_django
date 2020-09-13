from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)


class UserManager(BaseUserManager):

    def create_user(self, email, full_name, blood_group, phone, password=None, is_active=True, is_staff=False, is_admin=False):

        if not email:
            raise ValueError("User must have an Email-Address!")
        if not password:
            raise ValueError("User must have a Password!")
        if not full_name:
            raise ValueError("User must have a Full-Name!")
        if not blood_group:
            raise ValueError("User must have a Blood Group!")
        if not phone:
            raise ValueError("User must have a Mobile Number!")

        user_obj = self.model(
            email = self.normalize_email(email),
            full_name = full_name,
            blood_group = blood_group,
            phone = phone,
        )
        user_obj.staff  = is_staff
        user_obj.admin  = is_admin
        user_obj.active = is_active

        user_obj.set_password(password) # change user password
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, full_name, phone, blood_group, password=None):
        user = self.create_user(
            email,
            full_name,
            blood_group,
            phone,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, full_name, blood_group, phone, password=None):
        user = self.create_user(
            email,
            full_name,
            blood_group,
            phone,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user

    
class User(AbstractBaseUser):
    BLOOD_GROUPS = (
        ('A+' , 'A+'),
        ('B+' , 'B+'),
        ('AB+' , 'AB+'),
        ('O+' , 'O+'),
        ('A-' , 'A-'),
        ('B-' , 'B-'),
        ('AB-' , 'AB-'),
        ('O-' , 'O-'),
    )
    email         = models.EmailField(max_length=255, unique=True)
    full_name     = models.CharField(max_length=255) # extra add
    blood_group   = models.CharField(max_length=5, choices=BLOOD_GROUPS, default='B+', verbose_name="Blood Group") # extra add
    phone         = models.CharField(max_length=11, verbose_name='Mobile Number') # extra add
    active        = models.BooleanField(default=True)  # user can login
    staff         = models.BooleanField(default=False) # staff user non superuser
    admin         = models.BooleanField(default=False) # superuser
    timestamp     = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['full_name','blood_group','phone']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    class Meta:
        ordering = ['-timestamp',]


    



