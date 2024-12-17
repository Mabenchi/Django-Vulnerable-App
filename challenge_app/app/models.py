from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,UserManager

# class CustomUserManager(UserManager):
#     def _create_user(self, username, email, password, **extra_fields):
#         if not email:
#             raise ValueError("You have not provided a valid e-mail address")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self.db)
#         return user
    
#     def create_user(self, username=None, email=None, password=None, **extra_fields):
#         extra_fields.set_default('amount', 0)
#         return self._create_user(email, password, **extra_fields)

# class User(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(blank=True, default='', unique=True)
#     username = models.CharField(max_length=255, blank=True, default='',unique=True)

#     amount = models.DecimalField(max_digits=5,decimal_places=0, default=0)
    
#     date_joined = models.DateTimeField(default=timezone.now)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'username'
#     EMAIL_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     class Meta:
#         verbose_name = 'User'
#         verbose_name_plural = 'Users'
    
#     def get_full_name(self):
#         return self.username
#     def get_short_name(self):
#         return self.username