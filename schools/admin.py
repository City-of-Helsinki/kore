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
        return True


class NameTypeInline(nested_admin.NestedStackedInline):
    model = NameType
    extra = 0
    exclude = ('id', )


class SchoolNameInline(nested_admin.NestedTabularInline):
    model = SchoolName
    extra = 0
    exclude = ('id', 'reference', 'approx_begin', 'approx_end')
    inlines = [NameTypeInline]
    ordering = ('begin_year', 'begin_month', 'begin_day')


class SchoolContinuumActiveInline(nested_admin.NestedTabularInline):
    model = SchoolContinuum
    fk_name = 'active_school'
    extra = 0
    exclude = ('approx',)
    raw_id_fields = ('target_school',)
    autocomplete_lookup_fields = {
        'fk': ['target_school'],
    }
    ordering = ('year', 'month', 'day')


class SchoolContinuumTargetInline(nested_admin.NestedTabularInline):
    model = SchoolContinuum
    fk_name = 'target_school'
    extra = 0
    exclude = ('approx',)
    raw_id_fields = ('active_school',)
    autocomplete_lookup_fields = {
        'fk': ['active_school'],
    }
    ordering = ('year', 'month', 'day')


class LifeCycleEventInline(nested_admin.NestedTabularInline):
    model = LifecycleEvent
    extra = 0
    exclude = ('approx',)
    ordering = ('year', 'month', 'day')


class SchoolFieldInline(nested_admin.NestedTabularInline):
    model = SchoolField
    fk_name = 'school'
    extra = 0
    exclude = ('id', 'name_id')


class SchoolLanguageInline(nested_admin.NestedTabularInline):
    model = SchoolLanguage
    extra = 0


class SchoolTypeInline(nested_admin.NestedTabularInline):
    model = SchoolType
    fk_name = 'school'
    extra = 0
    exclude = ('main_school', 'reference', 'approx_begin', 'approx_end')
    ordering = ('begin_year', 'begin_month', 'begin_day')


class EmployershipInline(nested_admin.NestedTabularInline):
    model = Employership
    extra = 0
    exclude = ('id', 'nimen_id', 'reference', 'approx_begin', 'approx_end')
    raw_id_fields = ('principal',)
    autocomplete_lookup_fields = {
        'fk': ['principal'],
    }
    ordering = ('begin_year', 'begin_month', 'begin_day')


class SchoolBuildingInline(nested_admin.NestedTabularInline):
    model = SchoolBuilding
    extra = 0
    exclude = ('id', 'ownership', 'reference', 'approx_begin', 'approx_end')
    raw_id_fields = ('building',)
    autocomplete_lookup_fields = {
        'fk': ['building'],
    }
    ordering = ('begin_year', 'begin_month', 'begin_day')


@admin.register(School)
class SchoolAdmin(KoreAdmin):
    exclude = ('id', 'special_features', 'wartime_school', 'checked')
    list_display = ('__str__',)
    inlines = [SchoolNameInline,
               LifeCycleEventInline,
               SchoolContinuumActiveInline,
               SchoolContinuumTargetInline,
               SchoolBuildingInline,
               SchoolTypeInline,
               EmployershipInline]


class BuildingAddressInline(nested_admin.NestedTabularInline):
    model = BuildingAddress
    extra = 0


@admin.register(Building)
class BuildingAdmin(KoreAdmin):
    exclude = ('id', 'approx',)
    list_display = ('__str__',)
    inlines = [BuildingAddressInline]


@admin.register(Principal)
class PrincipalAdmin(KoreAdmin):
    exclude = ('id', 'approx',)
    list_display = ('__str__',)


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
