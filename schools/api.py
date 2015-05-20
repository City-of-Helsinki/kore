from rest_framework import routers, serializers, viewsets, mixins, filters
from .models import *


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


class SchoolTypeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolTypeName


class SchoolTypeSerializer(serializers.ModelSerializer):
    type = SchoolTypeNameSerializer()

    class Meta:
        model = SchoolType
        exclude = ('school',)


class SchoolFieldNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolFieldName


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


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address


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


class SchoolBuildingSerializer(serializers.ModelSerializer):
    building = BuildingSerializer()
    photos = SchoolBuildingPhotoSerializer(many=True)

    class Meta:
        model = SchoolBuilding
        exclude = ('school',)


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


class PrincipalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Principal
        # finite depth is required to prevent infinite loop
        depth = 2
        # fields must be declared here, because Employershipserializer isn't defined yet
        fields = ('url', 'id', 'surname', 'first_name', 'employers')


class EmployershipSerializer(serializers.ModelSerializer):
    principal = PrincipalSerializer()

    class Meta:
        model = Employership
        exclude = ('school', 'nimen_id')


class DataTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataType


class ArchiveDataSerializer(serializers.ModelSerializer):
    data_type = DataTypeSerializer()

    class Meta:
        model = ArchiveData
        exclude = ('id',)


class SchoolSerializer(serializers.HyperlinkedModelSerializer):
    names = SchoolNameSerializer(many=True)
    languages = SchoolLanguageSerializer(many=True)
    types = SchoolTypeSerializer(many=True)
    fields = SchoolFieldSerializer(many=True)
    genders = SchoolGenderSerializer(many=True)
    grade_counts = SchoolNumberOfGradesSerializer(many=True)
    buildings = SchoolBuildingSerializer(many=True)
    owners = SchoolOwnershipSerializer(many=True)
    founders = SchoolFounderSerializer(many=True)
    principals = EmployershipSerializer(many=True)
    archives = ArchiveDataSerializer(many=True, required=False)

    class Meta:
        model = School
        # fields must be declared here to explicitly include id along with url
        fields = ('url', 'id', 'names', 'languages', 'types', 'fields', 'genders',
                  'grade_counts', 'buildings', 'owners', 'founders', 'principals',
                  'special_features', 'wartime_school', 'nicknames', 'checked',
                  'archives')


class SchoolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('names__types__value',
                     'principals__principal__first_name',
                     'principals__principal__surname',
                     'buildings__building__buildingaddress__address__street_name_fi',
                     'buildings__building__buildingaddress__address__street_name_sv')


class PrincipalViewSet(mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    """
    Listing principals requires you to submit a query parameter for principal name
    """

    queryset = Principal.objects.all()
    serializer_class = PrincipalSerializer

router = routers.DefaultRouter()
router.register(r'school', SchoolViewSet)
router.register(r'principal', PrincipalViewSet)
