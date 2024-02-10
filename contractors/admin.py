from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Contractor, ExcelFile

admin.site.register(Contractor)
# admin.site.register(ExcelFile)

def export_excel(obj):
    url = reverse('download',args=[obj.id])
    return mark_safe(f'<a href="{url}">Download Sheet</a>')


@admin.register(ExcelFile)
class ExcelFileAdmin(admin.ModelAdmin):
    list_display = ['__str__', export_excel]
    list_filter = ['contractor']