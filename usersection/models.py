from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager)
from encrypted_fields.fields import EncryptedTextField, SearchField, EncryptedEmailField,EncryptedIntegerField,EncryptedCharField


# Create your models here.
class MyAccountManager(BaseUserManager):
    # We can pass extra parameters from the create_user function
    def create_user(self,email,username,password,fullname):
        if not email:
            raise ValueError("User must has an email.")
        if not username:
            raise ValueError("User must has username.")

        # Now passing the parameters & assigning the default values
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            fullname = fullname
        )

        # Setting password and saving in database
        user.set_password(password)
        user.save(using=self.db)
        return user


    # Creating superuser
    def create_superuser(self,email,username,password,fullname):
        # Now we're gonna pass parameters and creating super user
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            fullname = fullname,
            password = password
        )

        # Now we're gonna change the default values
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        # Saving admin
        user.save(using=self.db)
        return user


# Rewriting base user model
class Accounts(AbstractBaseUser):
    _fullname_data = EncryptedCharField(max_length=255, blank=True, null=True,verbose_name='fullname')
    fullname = SearchField(hash_key='1e3e1246ee77d9eb260ca706e5f30425124a5f1b9084539821e6858842a10ec3',encrypted_field_name='_fullname_data')
    email = models.EmailField(verbose_name='email',unique=True)
    _username_data = EncryptedCharField(max_length=100,blank=True, null=True,verbose_name='username')
    username = SearchField(hash_key='6eb7eea7ee801850ce5e4a79f6856b720d41126a8dd492a4c92788667b551e12',encrypted_field_name='_username_data')
    date_joined = models.DateTimeField(verbose_name="date joined",auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login",auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # Actually we're changing the email as login required
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username','fullname']

    objects = MyAccountManager()

    # function for returning email
    def __str__(self):
        return self.email
    # function for returning the is_admin
    def has_perm(self,perm,obj=None):
        return self.is_admin
    # giving permission to the admin
    def has_module_perms(self,app_label):
        return True
