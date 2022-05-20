from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


from djongo import models as M_models


class MyAccountManager(BaseUserManager):
    def create_user(self,username,email, password=None, ):

        if not username:
            raise ValueError('Username must have a username')
        

       
        user = self.model(
            username = username,
            email=email,
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,  username,email, password=None,):
        user = self.create_user(
            username = username,
            password=password,
            email = email
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True
        user.is_verified = True

        user.save(using=self._db)
        return user

        

class Account(AbstractBaseUser):
    
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100,unique=True)

    #required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    reset_password= models.BooleanField(default=False)

    is_superadmin = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email', ]
    USERNAME_FIELD = 'username'

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


# class Profile(models.Model):
#     phone = models.IntegerField(max_length=11, unique=True)
#     address=[

#     ]
    