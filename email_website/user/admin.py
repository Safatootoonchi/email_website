# web/admin.py
import json
from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth
from django.db.models import Q
from .models import User
from gmail.models import Email


class EmailAdmin(admin.TabularInline):
    model = Email
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ['email', 'name', 'phone', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser',
              'date_joined', 'date_of_birth', 'gender', 'country',
              ]
    inlines = [EmailAdmin]
    list_display = ["name", 'email', 'is_active', 'received_email', 'sent_email', 'space_used']

    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = (
            User.objects.annotate(date=TruncMonth("date_joined"))
                .values("date")
                .annotate(y=Count("id"))
                .order_by("-date")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)
