from django.contrib import admin
from .models import *


class SchoolBuildingPhotoInline(admin.TabularInline):
    model = SchoolBuildingPhoto


@admin.register(SchoolBuilding)
class SchoolBuildingAdmin(admin.ModelAdmin):
    fields = ('school', 'building', 'begin_year', 'end_year')
    readonly_fields = fields
    search_fields = ['school__names__types__value']
    list_display = ('__str__', 'has_photo')
    list_filter = ('photos',)
    inlines = [SchoolBuildingPhotoInline]
