from rest_framework import serializers
from .models import Email, Contact


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ["title", "to", "content", "cc", "bcc", "file", "user"]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["email", "name", "phone", "other_email", "birthday", "user"]
