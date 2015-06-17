from django.contrib import admin
from django.contrib.gis import admin as geo_admin
from .models import *

class ArchiveDataLinkInline(admin.TabularInline):
    model = ArchiveDataLink


@admin.register(ArchiveData)
class ArchiveDataAdmin(admin.ModelAdmin):
    fields = ('school', 'location')
    readonly_fields = fields
    search_fields = ['school__names__types__value', 'location']
    list_display = ('__str__', 'link')
    inlines = [ArchiveDataLinkInline]


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


class AddressHasLocationFilter(admin.SimpleListFilter):
    title = 'location'
    parameter_name = 'has_location'

    def lookups(self, request, model_admin):
        return (('1', 'yes'), ('0', 'no'))

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(location__isnull=False)
        else:
            return queryset.filter(location__isnull=True)


@admin.register(AddressLocation)
class AddressLocationAdmin(geo_admin.OSMGeoAdmin):
    default_lon = 2776460  # Central Railway Station in EPSG:3857
    default_lat = 8438120
    default_zoom = 12
    list_display = ('__str__', 'has_location', 'handmade')
    list_filter = (AddressHasLocationFilter, 'handmade', 'address__municipality_fi')
    ordering = ('address__street_name_fi',)

    def save_model(self, request, obj, form, change):
        obj.handmade = True
        return super(AddressLocationAdmin, self).save_model(request, obj, form, change)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    fields = ('street_name_fi',)
    readonly_fields = ('street_name_fi',)
