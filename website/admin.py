from django.contrib import admin

from .models import medicines, report_data

admin.site.register(report_data)
admin.site.register(medicines)
