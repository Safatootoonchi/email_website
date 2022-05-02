from django.db import models

# from email_website.user.models import User
from user.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from colorfield.fields import ColorField
from ckeditor.fields import RichTextField

# from .managers import EmailManager
import logging

logger = logging.getLogger("gmail")


class Email(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    to = models.CharField(max_length=100)
    # content = models.TextField(null=True, blank=True)
    content = RichTextField(blank=True, null=True)
    cc = models.CharField(max_length=300, null=True, blank=True)
    bcc = models.CharField(max_length=300, null=True, blank=True)
    file = models.FileField(null=True, upload_to="statics/file", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gmail_user")
    created_at = models.DateTimeField(default=timezone.now)
    draft = models.CharField(max_length=10, default="N")
    archive = models.CharField(max_length=10, default="N")
    show = models.CharField(max_length=10, default="Y")
    trash = models.DateTimeField(null=True)
    deleted = models.CharField(max_length=10, default="N")

    @property
    def file_size(self):
        if self.file and hasattr(self.file, "size"):
            return self.file.size


class Label(models.Model):
    user = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100, default="why")
    email = models.CharField(max_length=200, null=True, blank=True)
    due_date = models.CharField(max_length=200, null=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title


class Filter(models.Model):
    type_choices = [
        ("F", "From"),
        ("W", "has_the_word")
    ]
    filter_by = models.CharField(max_length=1, choices=type_choices)
    text = models.CharField(max_length=100, null=True)
    label = models.CharField(max_length=100, null=True, blank=True)
    user = models.CharField(max_length=100)
    draft = models.CharField(max_length=10, default="N")
    archive = models.CharField(max_length=10, default="N")


class Contact(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    other_email = models.EmailField(max_length=100, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    user = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "contacts"


class SearchContact(models.Model):
    type_choices = [
        ("E", "email"),
        ("N", "Name"),
        ("P", "Phone"),
        ("O", "Other email"),
        ("B", "Birthday"),
    ]
    type_search = models.CharField(max_length=1, choices=type_choices)


class Signature(models.Model):
    text = models.TextField(unique=True)
    user = models.CharField(max_length=200)


class EmailChart(models.Model):
    title = models.CharField(max_length=200)


class BackGround(models.Model):
    image = models.ImageField(null=True, upload_to="statics/background", blank=True)
    color = ColorField(default='#FF0000')


class Reply(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    content = RichTextField(blank=True, null=True)
    file = models.FileField(null=True, upload_to="statics/file", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reply_user")


class Forward(models.Model):
    to = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="forward_user")
