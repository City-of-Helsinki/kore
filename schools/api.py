from rest_framework import routers, serializers, viewsets, mixins, filters, relations
from munigeo.api import GeoModelSerializer
from rest_framework.serializers import ListSerializer, LIST_SERIALIZER_KWARGS

import datetime

from .models import *
import django_filters
from django import forms
from rest_framework.exceptions import ParseError


YEARS_OF_PRIVACY = 100

# for censoring principals in related instances

class CensoredManyRelatedField(relations.ManyRelatedField):
    """
    Handles view permissions for related field listings with Principal or Employership instances.
    """
    def to_representation(self, iterable):
        if iterable.model is Employership:
            iterable = iterable.filter(end_year__lt=datetime.datetime.now().year-YEARS_OF_PRIVACY)
        if iterable.mode is Principal:
            iterable.filter(employers__end_year__lt=datetime.datetime.now().year-YEARS_OF_PRIVACY)
        return super().to_representation(iterable)


class CensoredListSerializer(serializers.ListSerializer):
    """
    Handles view permissions for list serializers with Principal or Employership instances.
    """

    def to_representation(self, data):
        """
        List of object instances -> List of dicts of primitive datatypes.
        """
        # Dealing with nested relationships, data can be a Manager,
        # so, first get a queryset from the Manager if needed
        iterable = data.all() if isinstance(data, models.Manager) else data

        if iterable.model is Employership:
            iterable = iterable.filter(end_year__lt=datetime.datetime.now().year-YEARS_OF_PRIVACY)
        if iterable.model is Principal:
            iterable = iterable.filter(employers__end_year__lt=datetime.datetime.now().year-YEARS_OF_PRIVACY)
        return [
            self.child.to_representation(item) for item in iterable
        ]


class CensoredHyperlinkedRelatedField(relations.HyperlinkedRelatedField):
    """
    Handles view permissions for related field listings with Principal or Employership instances.
    """
    @classmethod
    def many_init(cls, *args, **kwargs):
        # the correct arguments must be passed on to the parent
        list_kwargs = {'child_relation': cls(*args, **kwargs)}
        for key in kwargs.keys():
            if key in relations.MANY_RELATION_KWARGS:
                list_kwargs[key] = kwargs[key]
        return CensoredManyRelatedField(**list_kwargs)


class CensoredHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    """
    Handles view permissions for related field listings with Principal or Employership instances.
    """
    serializer_related_field = CensoredHyperlinkedRelatedField

# the actual serializers


class SchoolNameSerializer(serializers.ModelSerializer):
    official_name = serializers.CharField(allow_null=True, source='get_official_name')
    other_names = serializers.ListField(
        source='get_other_names',
        child=serializers.DictField(child=serializers.CharField())
    )

    class Meta:
        model = SchoolName
        exclude = ('school',)


class SchoolLanguageSerializer(serializers.ModelSerializer):
    language = serializers.CharField(source='language.name')

    class Meta:
        model = SchoolLanguage
        exclude = ('school',)


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class SchoolTypeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolTypeName
        fields = '__all__'


class SchoolTypeNameViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SchoolTypeName.objects.all()
    serializer_class = SchoolTypeNameSerializer
    paginate_by = 50


class SchoolTypeSerializer(serializers.ModelSerializer):
    type = SchoolTypeNameSerializer()

    class Meta:
        model = SchoolType
        exclude = ('school',)


class SchoolFieldNameSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='description')

    class Meta:
        model = SchoolFieldName
        exclude = ('description',)


class SchoolFieldNameViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SchoolFieldName.objects.all()
    serializer_class = SchoolFieldNameSerializer


class SchoolFieldSerializer(serializers.ModelSerializer):
    field = SchoolFieldNameSerializer()

    class Meta:
        model = SchoolField
        exclude = ('school',)


class SchoolGenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolGender
        exclude = ('school',)


class SchoolNumberOfGradesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumberOfGrades
        exclude = ('school',)


class NeighborhoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neighborhood
        fields = '__all__'


class AddressLocationSerializer(GeoModelSerializer):
    class Meta:
        model = AddressLocation
        exclude = ('id', 'address')


class AddressSerializer(serializers.ModelSerializer):
    location = AddressLocationSerializer(required=False)

    def to_representation(self, obj):
        ret = super(AddressSerializer, self).to_representation(obj)
        if ret['location']:
            ret['location'] = ret['location']['location']
        return ret

    class Meta:
        model = Address
        fields = '__all__'


class DataTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataType
        fields = '__all__'


class ArchiveDataSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='link.url')
    data_type = DataTypeSerializer()

    class Meta:
        model = ArchiveData
        exclude = ('id',)


class OwnerFounderSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='type.description')

    class Meta:
        model = OwnerFounder
        fields = '__all__'


class SchoolOwnershipSerializer(serializers.ModelSerializer):
    owner = OwnerFounderSerializer()

    class Meta:
        model = SchoolOwnership
        exclude = ('school',)


class SchoolFounderSerializer(serializers.ModelSerializer):
    founder = OwnerFounderSerializer()

    class Meta:
        model = SchoolFounder
        exclude = ('school',)


class BuildingOwnershipSerializer(serializers.ModelSerializer):
    owner = OwnerFounderSerializer()

    class Meta:
        model = BuildingOwnership
        exclude = ('building',)


class SchoolBuildingPhotoSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        # we have to reformat the URL representation so that our API serves the corresponding photo URL
        # this method will have to be updated whenever Finna API changes!
        representation = super(SchoolBuildingPhotoSerializer, self).to_representation(instance)
        representation['url'] = representation['url'].replace(
            '.finna.fi/Record/',
            '.finna.fi/Cover/Show?id='
        ) + '&w=1200&h=1200'
        return representation

    class Meta:
        model = SchoolBuildingPhoto
        exclude = ('school_building',)


class BuildingForSchoolSerializer(serializers.ModelSerializer):
    neighborhood = serializers.CharField(source='neighborhood.name')
    addresses = AddressSerializer(many=True)
    owners = BuildingOwnershipSerializer(many=True)
    photos = serializers.ListField(
        source='get_photos',
        child=SchoolBuildingPhotoSerializer()
    )

    class Meta:
        model = Building
        # fields must be declared here to get both id and url
        fields = ('url', 'id', 'neighborhood', 'addresses', 'construction_year',
                  'architect', 'architect_firm', 'property_number', 'sliced',
                  'comment', 'reference', 'approx', 'owners', 'photos')


class PrincipalForSchoolSerializer(serializers.ModelSerializer):
    """
    This class is needed for the School endpoint
    """

    class Meta:
        model = Principal
        list_serializer_class = CensoredListSerializer
        # fields must be declared here to get both id and url
        fields = ('url', 'id', 'surname', 'first_name',)


class EmployershipForSchoolSerializer(serializers.ModelSerializer):
    principal = PrincipalForSchoolSerializer()

    class Meta:
        model = Employership
        list_serializer_class = CensoredListSerializer
        exclude = ('nimen_id',)


class SchoolBuildingForSchoolSerializer(serializers.ModelSerializer):
    """
    This class is needed for the School and Principal endpoints
    """
    photos = SchoolBuildingPhotoSerializer(many=True)
    building = BuildingForSchoolSerializer()

    class Meta:
        model = SchoolBuilding
        depth = 5
        # fields must be declared to get both id and url
        fields = ('url', 'id', 'building', 'photos', 'approx_begin', 'approx_end',
                  'begin_day', 'begin_month', 'begin_year', 'end_day', 'end_month', 'end_year',
                  'ownership', 'reference',)


class SchoolforSchoolContinuumSerializer(CensoredHyperlinkedModelSerializer):
    names = SchoolNameSerializer(many=True)

    class Meta:
        model = School
        # fields must be declared here to explicitly include id along with url
        fields = ('url', 'id', 'names')


class SchoolContinuumActiveSerializer(CensoredHyperlinkedModelSerializer):
    target_school = SchoolforSchoolContinuumSerializer()

    def to_representation(self, instance):
        # translate joins and separations to English
        representation = super().to_representation(instance)
        representation['description'] = representation['description'].replace(
            'yhdistyy', 'joins').replace('eroaa', 'separates from')
        return representation

    class Meta:
        model = SchoolContinuum
        fields = ('active_school', 'description', 'target_school', 'day', 'month', 'year',
                  'reference',)


class SchoolContinuumTargetSerializer(CensoredHyperlinkedModelSerializer):
    active_school = SchoolforSchoolContinuumSerializer()

    def to_representation(self, instance):
        # translate joins and separations to English
        representation = super().to_representation(instance)
        representation['description'] = representation['description'].replace(
            'yhdistyy', 'joins').replace('eroaa', 'separates from')
        return representation

    class Meta:
        model = SchoolContinuum
        fields = ('active_school', 'description', 'target_school', 'day', 'month', 'year',
                  'reference',)


class LifecycleEventSerializer(serializers.ModelSerializer):
    description = serializers.CharField(source='type.description')

    class Meta:
        model = LifecycleEvent
        fields = ('description', 'day', 'month', 'year', 'decisionmaker', 'additional_info')


class SchoolSerializer(CensoredHyperlinkedModelSerializer):
    names = SchoolNameSerializer(many=True)
    languages = SchoolLanguageSerializer(many=True)
    types = SchoolTypeSerializer(many=True)
    fields = SchoolFieldSerializer(many=True)
    genders = SchoolGenderSerializer(many=True)
    grade_counts = SchoolNumberOfGradesSerializer(many=True)
    buildings = SchoolBuildingForSchoolSerializer(many=True)
    owners = SchoolOwnershipSerializer(many=True)
    founders = SchoolFounderSerializer(many=True)
    principals = EmployershipForSchoolSerializer(many=True)
    archives = ArchiveDataSerializer(many=True, required=False)
    lifecycle_event = LifecycleEventSerializer(many=True, required=False)
    continuum_active = SchoolContinuumActiveSerializer(many=True, required=False)
    continuum_target = SchoolContinuumTargetSerializer(many=True, required=False)

    class Meta:
        model = School
        # fields must be declared here to explicitly include id along with url
        fields = ('url', 'id', 'names', 'languages', 'types', 'fields', 'genders',
                  'grade_counts', 'buildings', 'owners', 'founders', 'principals',
                  'special_features', 'wartime_school', 'nicknames', 'checked',
                  'archives', 'lifecycle_event', 'continuum_active', 'continuum_target')


class SchoolBuildingSerializer(CensoredHyperlinkedModelSerializer):
    photos = SchoolBuildingPhotoSerializer(many=True)
    school = SchoolSerializer()
    building = BuildingForSchoolSerializer()

    class Meta:
        model = SchoolBuilding
        depth = 5
        # fields must be declared to get both id and url
        fields = ('url', 'id', 'building', 'photos', 'school', 'approx_begin', 'approx_end',
                  'begin_day', 'begin_month', 'begin_year', 'end_day', 'end_month', 'end_year',
                  'ownership', 'reference',)


class EmployershipForPrincipalSerializer(serializers.ModelSerializer):
    school = SchoolSerializer()

    class Meta:
        model = Employership
        list_serializer_class = CensoredListSerializer
        exclude = ('nimen_id',)


class PrincipalSerializer(serializers.ModelSerializer):
    employers = EmployershipForPrincipalSerializer(many=True)

    class Meta:
        model = Principal
        # depth required to get all related data
        depth = 5
        # fields must be declared to get both id and url
        fields = ('url', 'id', 'surname', 'first_name', 'employers')


class EmployershipSerializer(EmployershipForSchoolSerializer):
    school = SchoolSerializer()

    class Meta:
        model = Employership
        exclude = ('nimen_id',)


class SchoolBuildingForBuildingSerializer(serializers.ModelSerializer):
    photos = SchoolBuildingPhotoSerializer(many=True)
    school = SchoolSerializer()

    class Meta:
        model = SchoolBuilding
        depth = 5
        # fields must be declared to get both id and url
        fields = ('url', 'id', 'photos', 'school', 'approx_begin', 'approx_end',
                  'begin_day', 'begin_month', 'begin_year', 'end_day', 'end_month', 'end_year',
                  'ownership', 'reference',)


class BuildingSerializer(serializers.ModelSerializer):
    neighborhood = serializers.CharField(source='neighborhood.name')
    addresses = AddressSerializer(many=True)
    schools = SchoolBuildingForBuildingSerializer(many=True)

    class Meta:
        model = Building
        exclude = ('photo',)


class InclusiveFilter(django_filters.Filter):
    """
    Filter for including entries where the field is null
    """

    def filter(self, qs, value):
        originalqs = super().filter(qs, value)
        self.lookup_expr = 'isnull'
        nullqs = super().filter(qs, value)
        return nullqs | originalqs


class InclusiveNumberFilter(InclusiveFilter):
    field_class = forms.DecimalField


class NameOrIdFilter(django_filters.Filter):
    """
    Filter that switches search target between name and "id", depending on input
    """
    table, underscore, column = "", "", ""

    def filter(self, qs, value):
        if str(value).isdigit():
            self.field_class = forms.DecimalField
            if not self.column:
                # store table and column name
                self.table, self.underscore, self.column = self.name.rpartition('__')
            # overwrite column name with column id
            self.name = self.table + '__id'
        else:
            self.field_class = forms.CharField
            if self.column:
                # overwrite column id with column name
                self.name = self.table + '__' + self.column
        return super().filter(qs, value)


class GenderFilter(django_filters.CharFilter):
    """
    Filter that maps letters m, f and c to hard-coded genders
    """

    GENDER_MAP = {
        'm': 'poikakoulu',
        'f': 'tyttökoulu',
        'c': 'tyttö- ja poikakoulu'
    }

    def filter(self, qs, value):
        if value in ([], (), {}, None, ''):
            return qs
        val = str(value).lower()
        if val not in self.GENDER_MAP and val not in self.GENDER_MAP.values():
            raise ParseError("Gender must be 'm', 'f' or 'c' (for coed)")
        value = self.GENDER_MAP.get(val, val)
        return super().filter(qs, value)


class SchoolFilter(django_filters.FilterSet):
    # the end year can be null, so we cannot use a default filter
    from_year = InclusiveNumberFilter(name="names__end_year", lookup_expr='gte')
    until_year = django_filters.NumberFilter(name="names__begin_year", lookup_expr='lte')
    type = NameOrIdFilter(name="types__type__name", lookup_expr='iexact')
    field = NameOrIdFilter(name="fields__field__description", lookup_expr='iexact')
    language = NameOrIdFilter(name="languages__language__name", lookup_expr='iexact')
    gender = GenderFilter(name="genders__gender", lookup_expr='iexact')

    class Meta:
        model = School
        fields = ['type',
                  'field',
                  'language',
                  'gender',
                  'from_year',
                  'until_year']


class SchoolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend)
    filter_class = SchoolFilter
    search_fields = ('names__types__value',)


class NameFilter(django_filters.CharFilter):
    """
    Filter that checks fields 'first_name' and 'surname'
    """
    table, underscore, column = "", "", ""

    def filter(self, qs, value):
        self.table, self.underscore, self.column = self.name.rpartition('__')
        if self.table:
            self.name = self.table + '__' + 'first_name'
        else:
            self.name = 'first_name'
        first_name_qs = super().filter(qs, value)
        if self.table:
            self.name = self.table + '__' + 'surname'
        else:
            self.name = 'surname'
        surname_qs = super().filter(qs, value)
        return first_name_qs | surname_qs


class PrincipalFilter(django_filters.FilterSet):
    # the end year can be null, so we cannot use a default filter
    from_year = InclusiveNumberFilter(name="employers__end_year", lookup_expr='gte')
    until_year = django_filters.NumberFilter(name="employers__begin_year", lookup_expr='lte')
    search = NameFilter(name="surname", lookup_expr='icontains')
    school_type = NameOrIdFilter(name="employers__school__types__type__name", lookup_expr='iexact')
    school_field = NameOrIdFilter(name="employers__school__fields__field__description", lookup_expr='iexact')
    school_language = NameOrIdFilter(name="employers__school__languages__language__name", lookup_expr='iexact')
    school_gender = GenderFilter(name="employers__school__genders__gender", lookup_expr='iexact')

    class Meta:
        model = Principal
        fields = ['search',
                  'from_year',
                  'until_year',
                  'school_type',
                  'school_field',
                  'school_language',
                  'school_gender']


class EmployershipFilter(django_filters.FilterSet):
    # the end year can be null, so we cannot use a default filter
    from_year = InclusiveNumberFilter(name="end_year", lookup_expr='gte')
    until_year = django_filters.NumberFilter(name="begin_year", lookup_expr='lte')
    search = NameFilter(name="principal__surname", lookup_expr='icontains')
    school_type = NameOrIdFilter(name="school__types__type__name", lookup_expr='iexact')
    school_field = NameOrIdFilter(name="school__fields__field__description", lookup_expr='iexact')
    school_language = NameOrIdFilter(name="school__languages__language__name", lookup_expr='iexact')
    school_gender = GenderFilter(name="school__genders__gender", lookup_expr='iexact')

    class Meta:
        model = Employership
        fields = ['search',
                  'from_year',
                  'until_year',
                  'school_type',
                  'school_field',
                  'school_language',
                  'school_gender']


class PrincipalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Principal.objects.filter(employers__end_year__lt=datetime.datetime.now().year-YEARS_OF_PRIVACY).distinct()
    serializer_class = PrincipalSerializer
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend)
    filter_class = PrincipalFilter


class EmployershipViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Employership.objects.filter(end_year__lt=datetime.datetime.now().year-YEARS_OF_PRIVACY)
    serializer_class = EmployershipSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = EmployershipFilter


class AddressFilter(django_filters.CharFilter):
    """
    Filter that checks fields 'street_name_fi' and 'street_name_sv'
    """

    def filter(self, qs, value):
        self.name = 'building__buildingaddress__address__street_name_fi'
        street_name_fi_qs = super().filter(qs, value)
        self.name = 'building__buildingaddress__address__street_name_sv'
        street_name_sv_qs = super().filter(qs, value)
        return street_name_fi_qs | street_name_sv_qs


class SchoolBuildingFilter(django_filters.FilterSet):
    # the end year can be null, so we cannot use a default filter
    from_year = InclusiveNumberFilter(name="end_year", lookup_expr='gte')
    until_year = django_filters.NumberFilter(name="begin_year", lookup_expr='lte')
    search = AddressFilter(name="building__buildingaddress__address__street_name_fi", lookup_expr='icontains')
    school_type = NameOrIdFilter(name="school__types__type__name", lookup_expr='iexact')
    school_field = NameOrIdFilter(name="school__fields__field__description", lookup_expr='iexact')
    school_language = NameOrIdFilter(name="school__languages__language__name", lookup_expr='iexact')
    school_gender = GenderFilter(name="school__genders__gender", lookup_expr='iexact')

    class Meta:
        model = SchoolBuilding
        fields = ['search',
                  'from_year',
                  'until_year',
                  'school_type',
                  'school_field',
                  'school_language',
                  'school_gender']


class BuildingFilter(django_filters.FilterSet):
    # the end year can be null, so we cannot use a default filter
    from_year = InclusiveNumberFilter(name="schools__end_year", lookup_expr='gte')
    until_year = django_filters.NumberFilter(name="schools__begin_year", lookup_expr='lte')
    search = AddressFilter(name="buildingaddress__address__street_name_fi", lookup_expr='icontains')
    school_type = NameOrIdFilter(name="schools__school__types__type__name", lookup_expr='iexact')
    school_field = NameOrIdFilter(name="schools__school__fields__field__description", lookup_expr='iexact')
    school_language = NameOrIdFilter(name="schools__school__languages__language__name", lookup_expr='iexact')
    school_gender = GenderFilter(name="schools__school__genders__gender", lookup_expr='iexact')

    class Meta:
        model = Building
        fields = ['search',
                  'from_year',
                  'until_year',
                  'school_type',
                  'school_field',
                  'school_language',
                  'school_gender']


class SchoolBuildingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SchoolBuilding.objects.all()
    serializer_class = SchoolBuildingSerializer
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend)
    filter_class = SchoolBuildingFilter


class BuildingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend)
    filter_class = BuildingFilter


router = routers.DefaultRouter()
router.register(r'school', SchoolViewSet)
router.register(r'principal', PrincipalViewSet)
router.register(r'employership', EmployershipViewSet)
router.register(r'school_field', SchoolFieldNameViewSet)
router.register(r'school_type', SchoolTypeNameViewSet)
router.register(r'language', LanguageViewSet)
router.register(r'building', BuildingViewSet)
router.register(r'school_building', SchoolBuildingViewSet)
