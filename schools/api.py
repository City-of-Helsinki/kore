from rest_framework import routers, serializers, viewsets
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

    class Meta:
        model = School


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

router = routers.DefaultRouter()
router.register(r'school', SchoolViewSet)
