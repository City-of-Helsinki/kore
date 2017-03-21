from django.contrib import admin
from django.contrib.gis import admin as geo_admin
import nested_admin
from .models import *


class KoreAdmin(nested_admin.NestedModelAdmin):
    """
    Makes sure the admin cannot delete schools or other kore data
    """

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return False


class SchoolNameInline(nested_admin.NestedTabularInline):
    model = SchoolName
    extra = 1
    exclude = ('id', 'reference', 'approx_begin', 'approx_end')


class SchoolFieldInline(nested_admin.NestedTabularInline):
    model = SchoolField
    fk_name = 'school'
    extra = 1
    exclude = ('id', 'name_id')


class SchoolLanguageInline(nested_admin.NestedTabularInline):
    model = SchoolLanguage
    extra = 1


class SchoolTypeInline(nested_admin.NestedTabularInline):
    model = SchoolType
    fk_name = 'school'
    extra = 1
    exclude = ('main_school', 'reference', 'approx_begin', 'approx_end')


class EmployershipInline(nested_admin.NestedTabularInline):
    model = Employership
    extra = 1
    exclude = ('id', 'nimen_id', 'reference', 'approx_begin', 'approx_end')


@admin.register(School)
class SchoolAdmin(KoreAdmin):
    exclude = ('id', 'special_features', 'wartime_school', 'checked')
    list_display = ('__str__',)
    inlines = [SchoolNameInline,
               SchoolTypeInline,
               EmployershipInline]


class ArchiveDataLinkInline(admin.TabularInline):
    model = ArchiveDataLink


@admin.register(ArchiveData)
class ArchiveDataAdmin(KoreAdmin):
    fields = ('school', 'location')
    readonly_fields = fields
    search_fields = ['school__names__types__value', 'location']
    list_display = ('__str__', 'link')
    inlines = [ArchiveDataLinkInline]


class SchoolBuildingPhotoInline(admin.TabularInline):
    model = SchoolBuildingPhoto


@admin.register(SchoolBuilding)
class SchoolBuildingAdmin(KoreAdmin):
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
