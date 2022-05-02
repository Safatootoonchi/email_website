from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
import gmail
from django.db.models import Q
from django.utils import timezone
from .managers import *

import logging

logger = logging.getLogger("user")


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    type_choices = [
        ("M", "Male"),
        ("F", "Female")
    ]
    gender = models.CharField(max_length=1, choices=type_choices, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()
    # username = str(name) + '@bt.com'
    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['email', 'phone']

    def received_email(self):
        count_of_email_received = gmail.models.Email.objects.filter(to=self.name).count()
        return count_of_email_received

    def sent_email(self):
        count_of_email_sent = gmail.models.Email.objects.filter(user=self.id).count()
        return count_of_email_sent

    def space_used(self):
        email_with_file = gmail.models.Email.objects.filter(file__isnull=False).exclude(file='')
        files_of_user = email_with_file.filter(Q(user=self) | Q(to=self.name))
        total = sum(int(objects.file_size) for objects in files_of_user)

        if total < 512000:
            total = total / 1024.0
            ext = 'kb'
        elif total < 4194304000:
            total = total / 1048576.0
            ext = 'mb'
        else:
            total = total / 1073741824.0
            ext = 'gb'
        return '%s %s' % (str(round(total, 2)), ext)

    def __str__(self):
        return self.email
