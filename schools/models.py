from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.forms import ValidationError
from munigeo.models import Address as Location
from django.utils.translation import ugettext_lazy as _

from schools.utils import geocode_address


class KoreModel(models.Model):
    """
    Contains the necessary permissions for separating historical and contemporary records.
    """

    def is_contemporary(self):
        """
        By default, a Kore object itself knows if it's historical or not.
        """
        if hasattr(self, 'end_year'):
            return not self.end_year
        else:
            # most objects without an end year are not temporal in the first place, certainly not contemporary
            return False

    class Meta:
        managed = False
        abstract = True
        permissions = (("change_history", _("Can change historical records")),)


class IncrementalIDKoreModel(KoreModel):
    """
    Needed as Django Autofield doesn't work with an existing database.
    """

    def save(self, **kwargs):
        if not self.id:
            print(self.__class__)
            self.id = self.__class__.objects.all().aggregate(models.Max('id'))['id__max']+1
            print(self.id)
        return super().save(kwargs)

    class Meta(KoreModel.Meta):
        abstract = True


class DataType(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    name = models.CharField(max_length=510, blank=True, db_column='nimi')

    def __str__(self):
        return str(self.name)

    class Meta:
        managed = False
        db_table = 'Aineistotyyppi'


class SchoolFieldName(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    description = models.CharField(max_length=510, blank=True, db_column='selite')

    def __str__(self):
        return str(self.description)

    class Meta:
        managed = False
        db_table = 'Ala'


class ArchiveData(IncrementalIDKoreModel):
    id = models.IntegerField(db_column='ID', primary_key=True)
    school = models.ForeignKey('School', null=True, db_column='koulun_id', related_name='archives')
    name = models.ForeignKey('SchoolName', null=True, db_column='nimen_id')
    data_type = models.ForeignKey(DataType, blank=True, null=True, db_column='aineistotyypin_id')
    location = models.CharField(max_length=510, blank=True, db_column='sijainti', verbose_name=_('location'))
    begin_year = models.IntegerField(blank=True, null=True, db_column='alkamisvuosi', verbose_name=_('start year'))
    end_year = models.IntegerField(blank=True, null=True, db_column='paattymisvuosi', verbose_name=_('end year'))
    arkiston_nimi = models.CharField(max_length=510, blank=True, db_column='arkiston_nimi')

    class Meta(KoreModel.Meta):
        db_table = 'Arkistoaineisto'
        verbose_name = _('archive data')
        verbose_name_plural = _('archive datas')

    def __str__(self):
        return str(self.school) + '/' + str(self.location) + ' (' + \
               str(self.begin_year) + '-' + (str(self.end_year) if self.end_year else '') + ')'


class LifecycleEvent(KoreModel):
    school = models.ForeignKey('School', db_column='koulun_id', related_name='lifecycle_event')
    type = models.ForeignKey('LifecycleEventType', db_column='elikaaritapahtuman_lajin_id', verbose_name=_('type'))
    day = models.IntegerField(blank=True, null=True, db_column='paiva', verbose_name=_('day'))
    month = models.IntegerField(blank=True, null=True, db_column='kuukausi', verbose_name=_('month'))
    year = models.IntegerField(db_column='vuosi', verbose_name=_('year'))
    decisionmaker = models.CharField(max_length=510, blank=True, db_column='paatoksen_tekija', verbose_name=_('decisionmaker'))
    decision_day = models.IntegerField(blank=True, null=True, db_column='paatoksen_paiva', verbose_name=_('decision day'))
    decision_month = models.IntegerField(blank=True, null=True, db_column='paatoksen_kuukausi', verbose_name=_('decision month'))
    decision_year = models.IntegerField(blank=True, null=True, db_column='paatoksen_vuosi', verbose_name=_('decision year'))
    additional_info = models.CharField(db_column='lis\xe4tietoja', max_length=510, blank=True, verbose_name=_('additional info'))
    reference = models.CharField(max_length=510, blank=True, db_column='viite', verbose_name=_('reference'))
    approx = models.BooleanField(default=False, db_column='noin')

    class Meta(KoreModel.Meta):
        db_table = 'Elinkaaritapahtuma'
        verbose_name = _('lifecycle event')
        verbose_name_plural = _('lifecycle events')


class LifecycleEventType(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    description = models.CharField(max_length=510, blank=True, db_column='selite')

    def __str__(self):
        return str(self.description)

    class Meta:
        managed = False
        db_table = 'Elinkaaritapahtuman_laji'


class SchoolContinuum(KoreModel):
    active_school = models.ForeignKey('School', db_column='koulun_a_id', related_name='continuum_active', verbose_name=_('active school'))
    description = models.CharField(max_length=510, blank=True, db_column='selite', verbose_name=_('description'))
    target_school = models.ForeignKey('School', db_column='koulun_b_id', related_name='continuum_target', verbose_name=_('target school'))
    day = models.IntegerField(blank=True, null=True, db_column='paiva', verbose_name=_('day'))
    month = models.IntegerField(blank=True, null=True, db_column='kuukausi', verbose_name=_('month'))
    year = models.IntegerField(blank=True, null=True, db_column='vuosi', verbose_name=_('year'))
    reference = models.CharField(max_length=510, blank=True, db_column='viite', verbose_name=_('reference'))
    approx = models.BooleanField(default=False, db_column='noin')

    class Meta(KoreModel.Meta):
        db_table = 'Jatkumo'
        verbose_name = _('continuum event')
        verbose_name_plural = _('continuum events')

    def __str__(self):
        return str(self.active_school) + ' ' + str(self.description) + ' ' + str(self.target_school)


class Neighborhood(KoreModel):
    id = models.IntegerField(db_column='ID', primary_key=True)
    name = models.CharField(max_length=510, blank=True, db_column='kaupunginosan_nimi')
    merge_day = models.IntegerField(blank=True, null=True, db_column='liittamispaiva')
    merge_month = models.IntegerField(blank=True, null=True, db_column='liittamiskuukausi')
    merge_year = models.IntegerField(blank=True, null=True, db_column='liittamisvuosi')

    def __str__(self):
        return self.name

    class Meta(KoreModel.Meta):
        db_table = 'Kaupunginosa'


class Language(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    name = models.CharField(max_length=510, blank=True, db_column='kielen_nimi')

    def __str__(self):
        return str(self.name)

    class Meta:
        managed = False
        db_table = 'Kieli'


class School(IncrementalIDKoreModel):
    id = models.AutoField(db_column='ID', primary_key=True)
    special_features = models.TextField(blank=True, db_column='erityispiirteet')
    wartime_school = models.BooleanField(default=False, db_column='sota_ajan_koulu')
    nicknames = models.CharField(max_length=510, blank=True, db_column='lempinimet', verbose_name=_('nicknames'))
    checked = models.BooleanField(default=False, db_column='tarkastettu')

    def __str__(self):
        types = NameType.objects.filter(name__school=self).order_by('-name__begin_year')\
            .filter(type='virallinen nimi')
        if not types:
            return '<no name>'
        else:
            return str(types[0].value)

    def is_contemporary(self):
        return self.names.filter(end_year__is_null=True)

    @staticmethod
    def autocomplete_search_fields():
        return ("names__types__value__icontains",)

    class Meta(KoreModel.Meta):
        db_table = 'Koulu'
        verbose_name = _('school')
        verbose_name_plural = _('schools')


class SchoolField(KoreModel):
    school = models.ForeignKey(School, db_column='koulun_id', related_name='fields')
    field = models.ForeignKey(SchoolFieldName, db_column='alan_id')
    main_school = models.ForeignKey(School, db_column='paakoulun_id', related_name='fields_main')
    begin_day = models.IntegerField(blank=True, null=True, db_column='alkamispaiva', verbose_name=_('begin day'))
    begin_month = models.IntegerField(blank=True, null=True, db_column='alkamiskuukausi', verbose_name=_('start month'))
    begin_year = models.IntegerField(blank=True, null=True, db_column='alkamisvuosi', verbose_name=_('start year'))
    approx_begin = models.BooleanField(default=False, db_column='noin_a')
    end_day = models.IntegerField(blank=True, null=True, db_column='paattymispaiva', verbose_name=_('end day'))
    end_month = models.IntegerField(blank=True, null=True, db_column='paattymiskuukausi', verbose_name=_('end month'))
    end_year = models.IntegerField(blank=True, null=True, db_column='paattymisvuosi', verbose_name=_('end year'))
    approx_end = models.BooleanField(default=False, db_column='noin_p')
    reference = models.CharField(max_length=510, blank=True, db_column='viite')

    def __str__(self):
        return str(self.field)

    def save(self, **kwargs):
        # the main school id must be set to the school id unless provided otherwise
        if not self.main_school_id:
            self.main_school_id = self.school_id
        return super().save(kwargs)

    class Meta(KoreModel.Meta):
        db_table = 'Koulun_ala'


class SchoolLanguage(KoreModel):
    school = models.ForeignKey(School, related_name='languages', db_column='koulun_id')
    language = models.ForeignKey(Language, db_column='kielen_id')
    begin_year = models.IntegerField(blank=True, null=True, db_column='alkamisvuosi', verbose_name=_('start year'))
    end_year = models.IntegerField(blank=True, null=True, db_column='paattymisvuosi', verbose_name=_('end year'))
    reference = models.CharField(max_length=510, blank=True, db_column='viite')
    approx_begin = models.BooleanField(default=False, db_column='noin_a')
    approx_end = models.BooleanField(default=False, db_column='noin_p')

    def __str__(self):
        return str(self.language)

    class Meta(KoreModel.Meta):
        db_table = 'Koulun_kieli'


class SchoolType(KoreModel):
    school = models.ForeignKey(School, db_column='koulun_id', related_name='types')
    type = models.ForeignKey('SchoolTypeName', db_column='koulutyypin_id', verbose_name=_('type'))
    main_school = models.ForeignKey(School, db_column='paakoulun_id', related_name='main_types')
    begin_day = models.IntegerField(blank=True, null=True, db_column='alkamispaiva', verbose_name=_('begin day'))
    begin_month = models.IntegerField(blank=True, null=True, db_column='alkamiskuukausi', verbose_name=_('start month'))
    begin_year = models.IntegerField(blank=True, null=True, db_column='alkamisvuosi', verbose_name=_('start year'))
    end_day = models.IntegerField(blank=True, null=True, db_column='paattymispaiva', verbose_name=_('end day'))
    end_month = models.IntegerField(blank=True, null=True, db_column='paattymiskuukausi', verbose_name=_('end month'))
    end_year = models.IntegerField(blank=True, null=True, db_column='paattymisvuosi', verbose_name=_('end year'))
    reference = models.CharField(max_length=510, blank=True, db_column='viite')
    approx_begin = models.BooleanField(default=False, db_column='noin_a')
    approx_end = models.BooleanField(default=False, db_column='noin_p')

    def __str__(self):
        return str(self.type)

    def save(self, **kwargs):
        # the main school id must be set to the school id unless provided otherwise
        if not self.main_school_id:
            self.main_school_id = self.school_id
        return super().save(kwargs)

    class Meta(KoreModel.Meta):
        db_table = 'Koulun_laatu'
        verbose_name = _('school type')
        verbose_name_plural = _('school types')


class SchoolOwnership(KoreModel):
    school = models.ForeignKey(School, related_name='owners', db_column='koulun_id')
    owner = models.ForeignKey('OwnerFounder', db_column='omistaja_perustajan_id')
    begin_day = models.IntegerField(blank=True, null=True, db_column='alkamispaiva', verbose_name=_('begin day'))
    begin_month = models.IntegerField(blank=True, null=True, db_column='alkamiskuukausi', verbose_name=_('start month'))
    begin_year = models.IntegerField(blank=True, null=True, db_column='alkamisvuosi', verbose_name=_('start year'))
    end_day = models.IntegerField(blank=True, null=True, db_column='paattymispaiva', verbose_name=_('end day'))
    end_month = models.IntegerField(blank=True, null=True, db_column='paattymiskuukausi', verbose_name=_('end month'))
    end_year = models.IntegerField(blank=True, null=True, db_column='paattymisvuosi', verbose_name=_('end year'))
    reference = models.CharField(max_length=510, blank=True, db_column='viite')
    approx_begin = models.BooleanField(default=False, db_column='noin_a')
    approx_end = models.BooleanField(default=False, db_column='noin_p')

    class Meta(KoreModel.Meta):
        db_table = 'Koulun_omistussuhde'


class SchoolFounder(KoreModel):
    school = models.ForeignKey(School, related_name='founders', db_column='koulun_id')
    founder = models.ForeignKey('OwnerFounder', db_column='omistaja_perustajan_id')
    reference = models.CharField(max_length=510, blank=True, db_column='viite')

    class Meta(KoreModel.Meta):
        db_table = 'Koulun_perustajat'


class SchoolGender(KoreModel):
    id = models.IntegerField(db_column='ID', primary_key=True)
    school = models.ForeignKey(School, related_name='genders', blank=True, null=True, db_column='koulun_id')
    gender = models.CharField(max_length=510, blank=True, db_column='sukupuoli')
    begin_day = models.IntegerField(blank=True, null=True, db_column='alkamispaiva', verbose_name=_('begin day'))
    begin_month = models.IntegerField(blank=True, null=True, db_column='alkamiskuukausi', verbose_name=_('start month'))
    begin_year = models.IntegerField(blank=True, null=True, db_column='alkamisvuosi', verbose_name=_('start year'))
    end_day = models.IntegerField(blank=True, null=True, db_column='paattymispaiva', verbose_name=_('end day'))
    end_month = models.IntegerField(blank=True, null=True, db_column='paattymiskuukausi', verbose_name=_('end month'))
    end_year = models.IntegerField(blank=True, null=True, db_column='paattymisvuosi', verbose_name=_('end year'))
    reference = models.CharField(max_length=510, blank=True, db_column='viite')
    approx_begin = models.BooleanField(default=False, db_column='noin_a')
    approx_end = models.BooleanField(default=False, db_column='noin_p')

    class Meta(KoreModel.Meta):
        db_table = 'Koulun_sukupuoli'


class SchoolTypeName(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    name = models.CharField(max_length=510, blank=True, db_column='selite')
    description = models.CharField(db_column='mit\xe4_se_tarkoittaa', max_length=510, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        managed = False
        db_table = 'Koulutyyppi'


class NumberOfGrades(KoreModel):
    id = models.IntegerField(db_column='ID', primary_key=True)
    school = models.ForeignKey(School, related_name='grade_counts', blank=True, null=True, db_column='koulun_id')
    number = models.IntegerField(blank=True, null=True, db_column='lukumaara')
    begin_day = models.IntegerField(blank=True, null=True, db_column='alkamispaiva', verbose_name=_('begin day'))
    begin_month = models.IntegerField(blank=True, null=True, db_column='alkamiskuukausi', verbose_name=_('start month'))
    begin_year = models.IntegerField(blank=True, null=True, db_column='alkamisvuosi', verbose_name=_('start year'))
    end_day = models.IntegerField(blank=True, null=True, db_column='paattymispaiva', verbose_name=_('end day'))
    end_month = models.IntegerField(blank=True, null=True, db_column='paattymiskuukausi', verbose_name=_('end month'))
    end_year = models.IntegerField(blank=True, null=True, db_column='paattymisvuosi', verbose_name=_('end year'))
    reference = models.CharField(max_length=510, blank=True, db_column='viite')
    approx_begin = models.BooleanField(default=False, db_column='noin_a')
    approx_end = models.BooleanField(default=False, db_column='noin_p')

    class Meta(KoreModel.Meta):
        db_table = 'Luokka-asteiden_lukumaara'


class NameType(IncrementalIDKoreModel):
    id = models.IntegerField(db_column='ID', primary_key=True)
    name = models.ForeignKey('SchoolName', blank=True, null=True, related_name='types', db_column='nimen_id')
    type = models.CharField(max_length=510, blank=True, db_column='nimen_tyyppi', default='virallinen nimi', verbose_name=_('name type'))
    value = models.CharField(max_length=510, blank=True, db_column='nimi', verbose_name=_('name'))

    def __str__(self):
        return str(self.type) + ': ' + str(self.value)

    class Meta(KoreModel.Meta):
        db_table = 'Nimen_tyyppi'
        verbose_name = _('name type')
        verbose_name_plural = _('name types')


class SchoolName(IncrementalIDKoreModel):
    id = models.IntegerField(db_column='ID', primary_key=True)
    school = models.ForeignKey(School, blank=True, null=True, related_name='names', db_column='koulun_id')
    begin_day = models.IntegerField(blank=True, null=True, db_column='alkamispaiva', verbose_name=_('begin day'))
    begin_month = models.IntegerField(blank=True, null=True, db_column='alkamiskuukausi', verbose_name=_('start month'))
    begin_year = models.IntegerField(blank=True, null=True, db_column='alkamisvuosi', verbose_name=_('start year'))
    end_day = models.IntegerField(blank=True, null=True, db_column='paattymispaiva', verbose_name=_('end day'))
    end_month = models.IntegerField(blank=True, null=True, db_column='paattymiskuukausi', verbose_name=_('end month'))
    end_year = models.IntegerField(blank=True, null=True, db_column='paattymisvuosi', verbose_name=_('end year'))
    reference = models.CharField(max_length=510, blank=True, db_column='viite')
    approx_begin = models.BooleanField(default=False, db_column='noin_a')
    approx_end = models.BooleanField(default=False, db_column='noin_p')

    def get_official_name(self):
        official_name = [x for x in self.types.all() if x.type == 'virallinen nimi']
        if official_name:
            return official_name[0].value
        else:
            return None

    def get_other_names(self):
        other_names = [x for x in self.types.all() if x.type != 'virallinen nimi']
        if other_names:
            return [{'type': x.type, 'value': x.value} for x in other_names]
        else:
            return None

    def __str__(self):
        return str(self.get_official_name())

    class Meta(KoreModel.Meta):
        db_table = 'Nimi'
        verbose_name = _('school name')
        verbose_name_plural = _('school names')


class OwnerFounder(KoreModel):
    id = models.IntegerField(db_column='ID', primary_key=True)
    name = models.CharField(max_length=510, blank=True, db_column='nimi')
    type = models.ForeignKey('OwnerFounderType', blank=True, null=True,
                             db_column='omistaja_perustajatyypin_id')

    class Meta(KoreModel.Meta):
        db_table = 'Omistaja_Perustaja'


class OwnerFounderType(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    description = models.CharField(max_length=510, blank=True, db_column='selite')

    class Meta:
        managed = False
        db_table = 'Omistaja_Perustajatyyppi'


class Address(IncrementalIDKoreModel):
    id = models.IntegerField(db_column='ID', primary_key=True)
    street_name_fi = models.CharField(max_length=510, blank=True, db_column='kadun_nimi_suomeksi', verbose_name=_('street name fi'))
    street_name_sv = models.CharField(max_length=510, blank=True, db_column='kadun_nimi_ruotsiksi')
    zip_code = models.CharField(max_length=510, blank=True, db_column='postitoimipaikka')
    municipality_fi = models.CharField(max_length=510, blank=True, db_column='kunnan_nimi_suomeksi')
    municipality_sv = models.CharField(max_length=510, blank=True, db_column='kunnan_nimi_ruotsiksi')
    begin_day = models.IntegerField(blank=True, null=True, db_column='alkamispaiva', verbose_name=_('begin day'))
    begin_month = models.IntegerField(blank=True, null=True, db_column='alkamiskuukausi', verbose_name=_('start month'))
    begin_year = models.IntegerField(blank=True, null=True, db_column='alkamisvuosi', verbose_name=_('start year'))
    end_day = models.IntegerField(blank=True, null=True, db_column='paattymispaiva', verbose_name=_('end day'))
    end_month = models.IntegerField(blank=True, null=True, db_column='paattymiskuukausi', verbose_name=_('end month'))
    end_year = models.IntegerField(blank=True, null=True, db_column='paattymisvuosi', verbose_name=_('end year'))
    comment = models.CharField(max_length=510, blank=True, db_column='kommentti')
    approx_begin = models.BooleanField(default=False, db_column='noin_a')
    approx_end = models.BooleanField(default=False, db_column='noin_p')

    class Meta(KoreModel.Meta):
        db_table = 'Osoite'
        verbose_name = _('address')
        verbose_name_plural = _('addresses')

    @staticmethod
    def autocomplete_search_fields():
        return ("street_name_fi__icontains",)

    def __str__(self):
        return str(self.street_name_fi) + ', ' + str(self.municipality_fi) + ' (' + \
               str(self.begin_year) + '-' + (str(self.end_year) if self.end_year else '') + ')'

    def clean(self):
        if not hasattr(self, 'location') or not self.location.handmade:
            if not self.municipality_fi:
                self.municipality_fi = 'Helsinki'
            munigeo_address = geocode_address(self.street_name_fi, self.municipality_fi)
            if not munigeo_address:
                raise ValidationError(
                    {'street_name_fi': _(
                        "Street address not found in %s. Please use a valid address or select the location manually on the map."
                    ) % self.municipality_fi})
            location = munigeo_address.location
            if self.location:
                self.changed_location = location
            else:
                self.location = AddressLocation(location=location)

    def save(self, **kwargs):
        saved = super().save()
        self.location.address = self
        if self.changed_location:
            self.location.location = self.changed_location
        self.location.save()
        return saved


class BuildingName(IncrementalIDKoreModel):
    id = models.IntegerField(db_column='ID', primary_key=True)
    name = models.CharField(max_length=510, blank=True, db_column='nimi')
    building = models.ForeignKey('Building', blank=True, null=True, db_column='rakennuksen_id',
                                 related_name='names')
    begin_year = models.IntegerField(blank=True, null=True, db_column='alkamisvuosi', verbose_name=_('start year'))
    end_year = models.IntegerField(blank=True, null=True, db_column='paattymisvuosi', verbose_name=_('end year'))
    reference = models.CharField(max_length=510, blank=True, db_column='viite')
    approx_begin = models.BooleanField(default=False, db_column='noin_a')
    approx_end = models.BooleanField(default=False, db_column='noin_p')

    class Meta(KoreModel.Meta):
        db_table = 'Rakennuksen_nimi'


class BuildingOwnership(KoreModel):
    building = models.ForeignKey('Building', db_column='rakennuksen_id', related_name='owners')
    owner = models.ForeignKey(OwnerFounder, db_column='omistaja_perustajan_id')
    begin_day = models.IntegerField(blank=True, null=True, db_column='alkamispaiva', verbose_name=_('begin day'))
    begin_month = models.IntegerField(blank=True, null=True, db_column='alkamiskuukausi', verbose_name=_('start month'))
    begin_year = models.IntegerField(blank=True, null=True, db_column='alkamisvuosi', verbose_name=_('start year'))
    end_day = models.IntegerField(blank=True, null=True, db_column='paattymispaiva', verbose_name=_('end day'))
    end_month = models.IntegerField(blank=True, null=True, db_column='paattymiskuukausi', verbose_name=_('end month'))
    end_year = models.IntegerField(blank=True, null=True, db_column='paattymisvuosi', verbose_name=_('end year'))
    reference = models.CharField(max_length=510, blank=True, db_column='viite')
    approx_begin = models.BooleanField(default=False, db_column='noin_a')
    approx_end = models.BooleanField(default=False, db_column='noin_p')

    class Meta(KoreModel.Meta):
        db_table = 'Rakennuksen_omistussuhde'


class BuildingAddress(KoreModel):
    building = models.ForeignKey('Building', db_column='rakennuksen_id', verbose_name=_('building'))
    address = models.ForeignKey(Address, db_column='osoitteen_id',
                                related_name='buildings', verbose_name=_('address'))

    class Meta(KoreModel.Meta):
        db_table = 'Rakennuksen_osoite'
        verbose_name = _('building address')
        verbose_name_plural = _('building addresses')


class SchoolBuilding(KoreModel):
    id = models.CharField(max_length=100, primary_key=True)
    school = models.ForeignKey(School, related_name='buildings', db_column='koulun_id')
    building = models.ForeignKey('Building', related_name='schools', db_column='rakennuksen_id', verbose_name=_('building'))
    ownership = models.BooleanField(default=False, db_column='omistus')
    begin_day = models.IntegerField(blank=True, null=True, db_column='alkamispaiva', verbose_name=_('begin day'))
    begin_month = models.IntegerField(blank=True, null=True, db_column='alkamiskuukausi', verbose_name=_('start month'))
    begin_year = models.IntegerField(blank=True, null=True, db_column='alkamisvuosi', verbose_name=_('start year'))
    end_day = models.IntegerField(blank=True, null=True, db_column='paattymispaiva', verbose_name=_('end day'))
    end_month = models.IntegerField(blank=True, null=True, db_column='paattymiskuukausi', verbose_name=_('end month'))
    end_year = models.IntegerField(blank=True, null=True, db_column='paattymisvuosi', verbose_name=_('end year'))
    reference = models.CharField(max_length=510, blank=True, db_column='viite')
    approx_begin = models.BooleanField(default=False, db_column='noin_a')
    approx_end = models.BooleanField(default=False, db_column='noin_p')

    def __str__(self):
        s = ''
        if self.begin_year:
            s += str(self.begin_year) + '-'
        if self.end_year:
            if not s:
                s += '-'
            s += str(self.end_year)

        return "%s / %s (%s)" % (self.school, self.building, s)

    def has_photo(self):
        return bool(self.photos.all())
    has_photo.boolean = True

    def save(self, **kwargs):
        if not self.id:
            self.id = str(self.school_id) + '-' + str(self.building_id)
        return super().save(kwargs)

    class Meta(KoreModel.Meta):
        db_table = 'Rakennuksen_status'
        ordering = ['school']
        verbose_name = _('school building')
        verbose_name_plural = _('school buildings')


class Building(IncrementalIDKoreModel):
    id = models.IntegerField(db_column='ID', primary_key=True)
    neighborhood = models.ForeignKey(Neighborhood, blank=True, null=True, db_column='kaupunginosan_id', verbose_name=_('neighborhood'))
    construction_year = models.IntegerField(blank=True, null=True, db_column='rakennusvuosi', verbose_name=_('construction year'))
    architect = models.CharField(max_length=510, blank=True, db_column='arkkitehti', verbose_name=_('architect'))
    architect_firm = models.CharField(max_length=510, blank=True, db_column='arkkitehtitoimisto', verbose_name=_('architect firm'))
    property_number = models.CharField(max_length=510, blank=True, db_column='kiinteistonumero', verbose_name=_('property number'))
    photo = models.BinaryField(blank=True, null=True, db_column='kuva')
    sliced = models.BooleanField(default=False, db_column='viipalerakennus', verbose_name=_('sliced'))
    comment = models.CharField(max_length=510, blank=True, db_column='kommentti')
    reference = models.CharField(max_length=510, blank=True, db_column='viite')
    approx = models.BooleanField(default=False, db_column='noin')
    addresses = models.ManyToManyField(Address, through=BuildingAddress)

    def __str__(self):
        addresses = self.addresses.order_by('-begin_year')
        s = None
        if addresses:
            s = addresses[0].street_name_fi
        if not s:
            s = '<no address>'
        names = self.names.order_by('-begin_year')
        if names:
            s += ' (%s)' % names[0].name
        if self.construction_year:
            s += ' (rak. %s)' % self.construction_year
        return s

    def get_photos(self):
        photos = []
        for school_building in self.schools.all():
            for photo in school_building.photos.all():
                photos.append(photo)
        return photos

    @staticmethod
    def autocomplete_search_fields():
        return ("addresses__street_name_fi__icontains",)

    class Meta(KoreModel.Meta):
        db_table = 'Rakennus'
        verbose_name = _('building')
        verbose_name_plural = _('buildings')


class Principal(IncrementalIDKoreModel):
    id = models.IntegerField(db_column='ID', primary_key=True)
    surname = models.CharField(max_length=510, blank=True, db_column='sukunimi')
    first_name = models.CharField(max_length=510, blank=True, db_column='etunimi')

    def __str__(self):
        return str(self.surname) + ', ' + str(self.first_name)

    def is_contemporary(self):
        return self.employers.filter(end_year__is_null=True)

    @staticmethod
    def autocomplete_search_fields():
        return ("surname__icontains", "first_name__icontains",)

    class Meta(KoreModel.Meta):
        db_table = 'Rehtori'
        verbose_name = _('principal')
        verbose_name_plural = _('principals')


class Employership(IncrementalIDKoreModel):
    id = models.IntegerField(db_column='ID', primary_key=True)
    school = models.ForeignKey(School, blank=True, null=True, related_name='principals', db_column='koulun_id')
    nimen_id = models.IntegerField(blank=True, null=True, db_column='nimen_id')
    principal = models.ForeignKey(Principal, blank=True, null=True, related_name='employers', db_column='rehtorin_id', verbose_name=_('principal'))
    begin_day = models.IntegerField(blank=True, null=True, db_column='alkamispaiva', verbose_name=_('begin day'))
    begin_month = models.IntegerField(blank=True, null=True, db_column='alkamiskuukausi', verbose_name=_('start month'))
    begin_year = models.IntegerField(blank=True, null=True, db_column='alkamisvuosi', verbose_name=_('start year'))
    end_day = models.IntegerField(blank=True, null=True, db_column='paattymispaiva', verbose_name=_('end day'))
    end_month = models.IntegerField(blank=True, null=True, db_column='paattymiskuukausi', verbose_name=_('end month'))
    end_year = models.IntegerField(blank=True, null=True, db_column='paattymisvuosi', verbose_name=_('end year'))
    reference = models.CharField(max_length=510, blank=True, db_column='viite')
    approx_begin = models.BooleanField(default=False, db_column='noin_a')
    approx_end = models.BooleanField(default=False, db_column='noin_p')

    def __str__(self):
        return str(self.principal) + ' - ' + str(self.school)

    class Meta(KoreModel.Meta):
        db_table = 'Tyosuhde'
        verbose_name = _('employership')
        verbose_name_plural = _('employerships')


class SchoolBuildingPhoto(KoreModel):
    school_building = models.ForeignKey(SchoolBuilding, related_name='photos')
    url = models.URLField()
    is_front = models.BooleanField(default=True, help_text=_("Is this a picture of the building front?"),
                                   verbose_name=_("is_front"))

    def __str__(self):
        return str(self.school_building)

    def is_contemporary(self):
        return self.school_building.is_contemporary()

    class Meta(KoreModel.Meta):
        managed = True
        verbose_name = _('school building photo')
        verbose_name_plural = _('school building photos')


class ArchiveDataLink(KoreModel):
    archive_data = models.OneToOneField(ArchiveData, related_name='link', db_index=True)
    url = models.URLField()

    def __str__(self):
        return str(self.url)

    def is_contemporary(self):
        return self.archive_data.is_contemporary()

    class Meta(KoreModel.Meta):
        managed = True
        verbose_name = _('archive data link')
        verbose_name_plural = _('archive data link')


class AddressLocation(KoreModel):
    address = models.OneToOneField(Address, related_name='location', db_index=True)
    location = models.PointField(srid=4326, null=True, blank=True)
    handmade = models.BooleanField(default=False, verbose_name=_("Update location by hand"),
                                   help_text=_("Select this if you want to update the location manually. Otherwise, the location will update automatically when you change the address."))

    objects = models.GeoManager()

    def has_location(self):
        return self.location is not None
    has_location.boolean = True

    def __str__(self):
        schools = School.objects.filter(buildings__building__addresses__location=self)
        if schools:
            schools_str = ' (%s)' % (', '.join([str(s) for s in schools]))
        else:
            schools_str = ''
        return str(self.address) + ' <=> ' + str(self.location) + schools_str

    def is_contemporary(self):
        return self.address.is_contemporary()

    class Meta(KoreModel.Meta):
        managed = True
        verbose_name = _('address location')
        verbose_name_plural = _('address locations')
