from rest_framework import routers, serializers, viewsets, mixins, filters
from munigeo.api import GeoModelSerializer
from .models import *
import django_filters
from django import forms
from rest_framework.exceptions import ParseError


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


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class SchoolTypeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolTypeName


class SchoolTypeNameViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SchoolTypeName.objects.all()
    serializer_class = SchoolTypeNameSerializer


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


class DataTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataType


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


class BuildingSerializer(serializers.ModelSerializer):
    neighborhood = serializers.CharField(source='neighborhood.name')
    addresses = AddressSerializer(many=True)

    class Meta:
        model = Building
        exclude = ('photo',)


class SchoolBuildingPhotoSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        # we have to reformat the URL representation so that our API serves the corresponding photo URL
        # this method will have to be updated whenever Finna API changes!
        representation = super(SchoolBuildingPhotoSerializer, self).to_representation(instance)
        representation['url'] = representation['url'].replace(
            '.finna.fi/Record/',
            '.finna.fi/thumbnail.php?id='
        ) + '&size=large'
        return representation

    class Meta:
        model = SchoolBuildingPhoto
        exclude = ('school_building',)


class PrincipalForSchoolSerializer(serializers.ModelSerializer):
    """
    This class is needed for the School endpoint
    """

    class Meta:
        model = Principal
        # fields must be declared here to get both id and url
        fields = ('url', 'id', 'surname', 'first_name',)


class EmployershipForSchoolSerializer(serializers.ModelSerializer):
    principal = PrincipalForSchoolSerializer()

    class Meta:
        model = Employership
        exclude = ('nimen_id',)


class SchoolBuildingForSchoolSerializer(serializers.ModelSerializer):
    """
    This class is needed for the School and Principal endpoints
    """
    photos = SchoolBuildingPhotoSerializer(many=True)
    building = BuildingSerializer()

    class Meta:
        model = SchoolBuilding
        depth = 5
        # fields must be declared to get both id and url
        fields = ('url', 'id', 'building', 'photos', 'approx_begin', 'approx_end',
                  'begin_day', 'begin_month', 'begin_year', 'end_day', 'end_month', 'end_year',
                  'ownership', 'reference',)


class SchoolContinuumSerializer(serializers.HyperlinkedModelSerializer):

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


class SchoolSerializer(serializers.HyperlinkedModelSerializer):
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
    continuum_active = SchoolContinuumSerializer(many=True, required=False)
    continuum_target = SchoolContinuumSerializer(many=True, required=False)

    class Meta:
        model = School
        # fields must be declared here to explicitly include id along with url
        fields = ('url', 'id', 'names', 'languages', 'types', 'fields', 'genders',
                  'grade_counts', 'buildings', 'owners', 'founders', 'principals',
                  'special_features', 'wartime_school', 'nicknames', 'checked',
                  'archives', 'continuum_active', 'continuum_target')


class SchoolBuildingSerializer(serializers.ModelSerializer):
    photos = SchoolBuildingPhotoSerializer(many=True)
    school = SchoolSerializer()
    building = BuildingSerializer()

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
        exclude = ('nimen_id',)


class PrincipalSerializer(serializers.ModelSerializer):
    employers = EmployershipForPrincipalSerializer(many=True)

    class Meta:
        model = Principal
        # depth required to get all related data
        depth = 5
        # fields must be declared to get both id and url
        fields = ('url', 'id', 'surname', 'first_name', 'employers')


class InclusiveFilter(django_filters.Filter):
    """
    Filter for including entries where the field is null
    """

    def filter(self, qs, value):
        originalqs = super().filter(qs, value)
        self.lookup_type = 'isnull'
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
    from_year = InclusiveNumberFilter(name="names__end_year", lookup_type='gte')
    until_year = django_filters.NumberFilter(name="names__begin_year", lookup_type='lte')
    type = NameOrIdFilter(name="types__type__name", lookup_type='iexact')
    field = NameOrIdFilter(name="fields__field__description", lookup_type='iexact')
    language = NameOrIdFilter(name="languages__language__name", lookup_type='iexact')
    gender = GenderFilter(name="genders__gender", lookup_type='iexact')

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

    def filter(self, qs, value):
        self.name = 'first_name'
        first_name_qs = super().filter(qs, value)
        self.name = 'surname'
        surname_qs = super().filter(qs, value)
        return first_name_qs | surname_qs


class ObligatoryNameFilter(NameFilter):
    """
    Filter that does not allow queries shorter than four characters
    """

    def filter(self, qs, value):
        if len(str(value)) < 4:
            raise ParseError("You must enter at least four characters in ?search=")
        return super().filter(qs, value)


class PrincipalFilter(django_filters.FilterSet):
    # the end year can be null, so we cannot use a default filter
    from_year = InclusiveNumberFilter(name="employers__end_year", lookup_type='gte')
    until_year = django_filters.NumberFilter(name="employers__begin_year", lookup_type='lte')
    # all principals may not be listed
    search = ObligatoryNameFilter(name="surname", lookup_type='icontains')

    class Meta:
        model = Principal
        fields = ['search',
                  'from_year',
                  'until_year']


class SinglePrincipalViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Principal.objects.all()
    serializer_class = PrincipalSerializer


class PrincipalViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Please enter principal name in ?search=
    """

    queryset = Principal.objects.all()
    serializer_class = PrincipalSerializer
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend)
    filter_class = PrincipalFilter


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
    from_year = InclusiveNumberFilter(name="end_year", lookup_type='gte')
    until_year = django_filters.NumberFilter(name="begin_year", lookup_type='lte')
    search = AddressFilter(name="building__buildingaddress__address__street_name_fi", lookup_type='icontains')

    class Meta:
        model = SchoolBuilding
        fields = ['search',
                  'from_year',
                  'until_year']


class SchoolBuildingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SchoolBuilding.objects.all()
    serializer_class = SchoolBuildingSerializer
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend)
    filter_class = SchoolBuildingFilter


router = routers.DefaultRouter()
router.register(r'school', SchoolViewSet)
router.register(r'principal', SinglePrincipalViewSet)
router.register(r'principal', PrincipalViewSet)
router.register(r'school_field', SchoolFieldNameViewSet)
router.register(r'school_type', SchoolTypeNameViewSet)
router.register(r'language', LanguageViewSet)
router.register(r'school_building', SchoolBuildingViewSet)
