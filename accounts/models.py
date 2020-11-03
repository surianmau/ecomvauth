from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username ,password=None,is_staff=False,is_active=True,is_admin=False):
        if not username:
            raise ValueError('user must have a phone number')
        if not password:
            raise ValueError('user must have a password')

        user_obj = self.model(
            username=username
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self.db)
        return user_obj

    def create_staffuser(self,username,password=None):
        user = self.create_user(
            username,
            password=password,
            is_staff=True,
        )
        return user
    def create_superuser(self,username,password=None):
        user =self.create_user(
            username,
            password=password,
            is_admin=True,
            is_staff=True
        )
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=150 , unique=True)
    first_login =models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    staff  = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        if self.username:
            return self.username
        else:
            return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin
    @property
    def is_active(self):
        return self.active

