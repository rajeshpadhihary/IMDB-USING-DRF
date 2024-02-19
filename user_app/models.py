from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser


class MyAccountManager(BaseUserManager):
    def create_user(self, Email_Address, name=None, birthday=None, zipcode=None,password=None):
        if not Email_Address:
            raise ValueError('Users must have an email address')

        user = self.model(
            Email_Address=self.normalize_email(Email_Address),
            name=name,
            Date_of_Birth=birthday,
            zipcode=zipcode,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, Email_Address, password):
        user = self.create_user(
            Email_Address=self.normalize_email(Email_Address),
            password=password,
        )
        user.is_admin = True
        user.is_active=True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

class Users(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    Email_Address = models.EmailField(max_length=60, unique=True, blank=True, null=True, default=None)
    Date_of_Birth = models.CharField(max_length=30, blank=True, null=True, default=None)
    name = models.CharField(max_length=30, blank=True, null=True)
    username= models.CharField(max_length=30,unique=True, blank=True, null=True)
    zipcode = models.CharField(max_length=30, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'Email_Address'

    objects = MyAccountManager()

    class Meta:
        db_table = "tbl_users"

    def __str__(self):
        return str(self.Email_Address)


    def has_perm(self, perm, obj=None): return self.is_superuser

    def has_module_perms(self, app_label): return self.is_superuser
