from rest_framework import routers, serializers, viewsets
from .models import *


class SchoolNameSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        ret = super().to_representation(obj)
        names = obj.types.all()
        official_name = [n for n in names if n.type == 'virallinen nimi']

        ret['names'] = [{'type': x.type, 'value': x.value} for x in names]
        return ret

    class Meta:
        model = SchoolName
        exclude = ('id', 'school')


class SchoolSerializer(serializers.HyperlinkedModelSerializer):
    names = SchoolNameSerializer(many=True, read_only=True)

    class Meta:
        model = School


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

router = routers.DefaultRouter()
router.register(r'school', SchoolViewSet)
