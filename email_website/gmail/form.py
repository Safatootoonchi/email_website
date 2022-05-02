from django import forms
from django.core.exceptions import ValidationError
from .models import Email, Label, Filter, Contact, SearchContact, Signature, Reply, Forward
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _
from django.conf import settings

MAX_UPLOAD_SIZE = "26214400"


class EmailModelForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ["title", "to", "content", "cc", "bcc", "file"]

    def clean(self):
        self.check_file()
        return self.cleaned_data

    def check_file(self):
        content = self.cleaned_data["file"]
        if content:
            content_type = content.content_type.split('/')[0]
            if content.size > int(MAX_UPLOAD_SIZE):
                raise forms.ValidationError(_("Please keep file size under %s. Current file size %s") % (
                    filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(content.size)))
            return content


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ["title"]


class FilterForm(forms.ModelForm):
    class Meta:
        model = Filter
        fields = ["filter_by", "text", "label"]


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["email", "name", "phone", "other_email", "birthday"]


class SearchContactForm(forms.ModelForm):
    class Meta:
        model = SearchContact
        fields = ["type_search"]


class SignatureForm(forms.ModelForm):
    class Meta:
        model = Signature
        fields = ["text"]


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ["title", "content", "file"]


class ForwardForm(forms.ModelForm):
    class Meta:
        model = Forward
        fields = ["to"]
