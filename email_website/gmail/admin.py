# web/admin.py
import json

from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth
from django.db.models import Q
from .models import Email, EmailChart, Label, BackGround
from user.models import User


def sizify(value):
    """
    Simple kb/mb/gb size:
    """
    # value = ing(value)
    if value < 512000:
        value = value / 1024.0
        ext = 'kb'
    elif value < 4194304000:
        value = value / 1048576.0
        ext = 'mb'
    else:
        value = value / 1073741824.0
        ext = 'gb'
    return '%s %s' % (str(round(value, 2)), ext)


@admin.register(Email)
class EmailSubscriberAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "to", "content", "cc", "bcc", "file", "user", "created_at"]
    ordering = ("-created_at",)

    def get_user_storage(self, obj):
        user_files = Email.objects.filter(user=obj.email).exclude(file=None)
        total = sum(int(objects.file_size) for objects in user_files if objects.file_size)

        total = sizify(total)
        return total

    get_user_storage.short_description = 'Storage Used'

    def changelist_view(self, request, extra_context=None):
        email_with_file = Email.objects.filter(file__isnull=False).exclude(file='')
        all_email = Email.objects.all()
        all_user = User.objects.all()
        print(all_user)
        file_date = []
        for user in all_user:
            files_of_user = email_with_file.filter(Q(user=user) | Q(to=user.name))
            total = sum(int(objects.file_size) for objects in files_of_user)
            count_of_user = all_email.filter(Q(user=user) | Q(to=user.name))
            f_count = count_of_user.count()
            file_date.append({'user': user.name, 'user_size': total, 'user_count': f_count})
            extra_context = extra_context or {'file_data': file_date}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(EmailChart)
class ChartAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = (
            Email.objects.annotate(date=TruncMonth("created_at"))
                .values("date")
                .annotate(y=Count("id"))
                .order_by("-date")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    fields = ["title"]
    list_display = ["title"]


@admin.register(BackGround)
class BackGroundAdmin(admin.ModelAdmin):
    fields = ["image", "color"]
