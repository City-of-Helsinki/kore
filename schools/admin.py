from django.contrib import admin
from django.contrib.gis import admin as geo_admin
import nested_admin
from leaflet.admin import LeafletGeoAdminMixin

from .models import *
from django.utils.translation import ugettext_lazy as _


class KoreAdmin(nested_admin.NestedModelAdmin):
    """
    Makes sure the admin cannot delete schools or other kore data
    """

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        """
        Admin user is either allowed to edit all objects, or only contemporary data. Contemporaneity of
        the data is deduced on a model by model basis on the presence of end_year, and requires
        implementing is_contemporary method in each model.
        """
        if obj and not request.user.has_perm('schools.change_history') and not obj.is_contemporary():
            return False
        return super().has_change_permission(request, obj)


class ContemporaryFilter(admin.SimpleListFilter):
    title = _('contemporary or historical')
    parameter_name = 'is_contemporary'

    def lookups(self, request, model_admin):
        return (('1', _('contemporary')), ('0', _('historical')))

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(end_year__isnull=True)
        if self.value() == '0':
            return queryset.filter(end_year__isnull=False)
        else:
            return queryset


class ContemporaryPrincipalFilter(ContemporaryFilter):

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.exclude(employers=None).filter(employers__end_year__isnull=True)
        if self.value() == '0':
            return queryset.filter(employers__end_year__isnull=False)
        else:
            return queryset


class ContemporarySchoolFilter(ContemporaryFilter):

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(names__end_year__isnull=True)
        if self.value() == '0':
            return queryset.filter(names__end_year__isnull=False)
        else:
            return queryset


class ContemporaryBuildingFilter(ContemporaryFilter):

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(schools__end_year__isnull=True)
        if self.value() == '0':
            return queryset.filter(schools__end_year__isnull=False)
        else:
            return queryset


class NameTypeInline(nested_admin.NestedStackedInline):
    model = NameType
    extra = 0
    exclude = ('id', )
    verbose_name = _("")


class SchoolNameInline(nested_admin.NestedTabularInline):
    model = SchoolName
    extra = 0
    exclude = ('id', 'reference', 'approx_begin', 'approx_end')
    inlines = [NameTypeInline]
    ordering = ('begin_year', 'begin_month', 'begin_day')
    classes = ('grp-collapse grp-open',)


class SchoolContinuumActiveInline(nested_admin.NestedTabularInline):
    model = SchoolContinuum
    fk_name = 'active_school'
    verbose_name = _("Action targeting another school")
    verbose_name_plural = _("Actions targeting another school")
    extra = 0
    exclude = ('approx', 'reference')
    raw_id_fields = ('target_school',)
    autocomplete_lookup_fields = {
        'fk': ['target_school'],
    }
    ordering = ('year', 'month', 'day')
    classes = ('grp-collapse grp-open',)


class SchoolContinuumTargetInline(nested_admin.NestedTabularInline):
    model = SchoolContinuum
    fk_name = 'target_school'
    verbose_name = _("Action targeting this school")
    verbose_name_plural = _("Actions targeting this school")
    extra = 0
    exclude = ('approx', 'reference')
    raw_id_fields = ('active_school',)
    autocomplete_lookup_fields = {
        'fk': ['active_school'],
    }
    ordering = ('year', 'month', 'day')
    classes = ('grp-collapse grp-open',)


class LifeCycleEventInline(nested_admin.NestedTabularInline):
    model = LifecycleEvent
    extra = 0
    exclude = ('approx', 'decisionmaker', 'decision_day', 'decision_month', 'decision_year', 'additional_info', 'reference')
    ordering = ('year', 'month', 'day')
    classes = ('grp-collapse grp-open',)


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
    classes = ('grp-collapse grp-open',)


class EmployershipInline(nested_admin.NestedTabularInline):
    model = Employership
    extra = 0
    exclude = ('id', 'nimen_id', 'reference', 'approx_begin', 'approx_end')
    raw_id_fields = ('principal',)
    autocomplete_lookup_fields = {
        'fk': ['principal'],
    }
    ordering = ('begin_year', 'begin_month', 'begin_day')
    classes = ('grp-collapse grp-open',)


class SchoolBuildingPhotoInline(admin.TabularInline):
    model = SchoolBuildingPhoto
    extra = 0


class SchoolBuildingInline(nested_admin.NestedTabularInline):
    model = SchoolBuilding
    extra = 0
    exclude = ('id', 'ownership', 'reference', 'approx_begin', 'approx_end')
    raw_id_fields = ('building',)
    autocomplete_lookup_fields = {
        'fk': ['building'],
    }
    ordering = ('begin_year', 'begin_month', 'begin_day')
    classes = ('grp-collapse grp-open',)
    inlines = [SchoolBuildingPhotoInline]


class ArchiveDataLinkInline(admin.TabularInline):
    model = ArchiveDataLink


class ArchiveDataInline(nested_admin.NestedTabularInline):
    model = ArchiveData
    fields = ('school', 'location', 'begin_year', 'end_year')
    extra = 0
    ordering = ('end_year',)
    classes = ('grp-collapse grp-open',)
    inlines = [ArchiveDataLinkInline]


class UnitNumberInline(nested_admin.NestedTabularInline):
    model = SchoolUnitNumber
    exclude = ()
    extra = 0
    ordering = ('end_year',)
    classes = ('grp-collapse grp-open',)


@admin.register(School)
class SchoolAdmin(KoreAdmin):
    exclude = ('id', 'wartime_school', 'checked')
    list_display = ('__str__',)
    list_filter = ('types__type', ContemporarySchoolFilter,)
    search_fields = ['names__types__value', 'unit_numbers__number']
    inlines = [UnitNumberInline,
               SchoolNameInline,
               LifeCycleEventInline,
               SchoolContinuumActiveInline,
               SchoolContinuumTargetInline,
               SchoolBuildingInline,
               SchoolTypeInline,
               EmployershipInline,
               ArchiveDataInline]
    ordering = ('-names__begin_year',)


class BuildingAddressInline(nested_admin.NestedTabularInline):
    model = BuildingAddress
    extra = 0
    raw_id_fields = ('address',)
    classes = ('grp-collapse grp-open',)
    autocomplete_lookup_fields = {
        'fk': ['address'],
    }


class SchoolBuildingInlineForBuilding(SchoolBuildingInline):
    raw_id_fields = ('school',)
    autocomplete_lookup_fields = {
        'fk': ['school'],
    }
    verbose_name = _('School in this building')
    verbose_name_plural = _('Schools in this building')


@admin.register(Building)
class BuildingAdmin(KoreAdmin):
    exclude = ('id', 'approx', 'comment', 'reference')
    search_fields = ['addresses__street_name_fi']
    list_display = ('__str__',)
    list_filter = (ContemporaryBuildingFilter,)
    inlines = [BuildingAddressInline,
               SchoolBuildingInlineForBuilding]
    ordering = ('addresses__street_name_fi',)


class EmployershipInlineForPrincipal(EmployershipInline):
    raw_id_fields = ('school',)
    autocomplete_lookup_fields = {
        'fk': ['school'],
    }


@admin.register(Principal)
class PrincipalAdmin(KoreAdmin):
    fields = ('surname', 'first_name',)
    search_fields = ['surname', 'first_name']
    list_display = ('__str__',)
    list_filter = (ContemporaryPrincipalFilter,)
    inlines = [EmployershipInlineForPrincipal]
    ordering = ('surname', 'first_name')


@admin.register(ArchiveData)
class ArchiveDataAdmin(KoreAdmin):
    fields = ('school', 'location', 'begin_year', 'end_year')
    readonly_fields = fields
    search_fields = ['school__names__types__value', 'location']
    list_display = ('__str__', 'link')
    list_filter = (ContemporaryFilter, 'location',)
    inlines = [ArchiveDataLinkInline]
    ordering = ('end_year',)


#@admin.register(SchoolBuilding)
class SchoolBuildingAdmin(KoreAdmin):
    fields = ('school', 'building', 'begin_year', 'end_year')
    readonly_fields = fields
    search_fields = ['school__names__types__value']
    list_display = ('__str__', 'has_photo')
    list_filter = (ContemporaryFilter,)
    inlines = [SchoolBuildingPhotoInline]


class AddressHasLocationFilter(admin.SimpleListFilter):
    title = 'location'
    parameter_name = 'has_location'

    def lookups(self, request, model_admin):
        return (('1', 'yes'), ('0', 'no'))

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(location__isnull=False)
        if self.value() == '0':
            return queryset.filter(location__isnull=True)
        else:
            return queryset


#@admin.register(AddressLocation)
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


class AddressLocationInline(LeafletGeoAdminMixin, nested_admin.NestedTabularInline):
    map_width = '800px'
    model = AddressLocation
    fields = ('location','handmade')
    settings_overrides = {
        'DEFAULT_CENTER': (60.192059, 24.945831),  # Helsinki
        'DEFAULT_ZOOM': 11,
        'MIN_ZOOM': 6,
        'MAX_ZOOM': 16,
        'SPATIAL_EXTENT': (24.8, 60.1, 25.1, 60.3)
    }

    def save_model(self, request, obj, form, change):
        obj.handmade = True
        return super().save_model(request, obj, form, change)


class BuildingAddressInlineForAddress(BuildingAddressInline):
    raw_id_fields = ('building',)
    autocomplete_lookup_fields = {
        'fk': ['building'],
    }
    verbose_name = _('Building in this address')
    verbose_name_plural = _('Buildings in this address')


@admin.register(Address)
class AddressAdmin(KoreAdmin):
    fields = ('street_name_fi', 'begin_day', 'begin_month', 'begin_year',
              'end_day', 'end_month', 'end_year')
    search_fields = ['street_name_fi']
    list_filter = (ContemporaryFilter,)
    inlines = [AddressLocationInline, BuildingAddressInlineForAddress]
    ordering = ('street_name_fi',)
