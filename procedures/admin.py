from django.contrib import admin

from .models import Procedure


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    """Лоты"""
    list_display = ("docPublishDate", "purchaseObjectInfo", "regNum", "fullName", "maxPrice", "curator")
    list_filter = ("curator",)

