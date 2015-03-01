from __future__ import unicode_literals

from django.db import models


class DataType(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    name = models.CharField(max_length=510, blank=True, db_column='nimi')

    class Meta:
        managed = False
        db_table = 'Aineistotyyppi'


class Field(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    description = models.CharField(max_length=510, blank=True, db_column='selite')

    class Meta:
        managed = False
        db_table = 'Ala'


class ArchiveData(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    school = models.ForeignKey('School', blank=True, null=True, db_column='koulun_id')
    nimen_id = models.IntegerField(blank=True, null=True, db_column='nimen_id')
    datatype = models.ForeignKey(DataType, blank=True, null=True, db_column='aineistotyypin_id')
    location = models.CharField(max_length=510, blank=True, db_column='sijainti')
    begin_year = models.IntegerField(blank=True, null=True, db_column='alkamisvuosi')
    end_year = models.IntegerField(blank=True, null=True, db_column='paattymisvuosi')
    arkiston_nimi = models.CharField(max_length=510, blank=True, db_column='arkiston_nimi')

    class Meta:
        managed = False
        db_table = 'Arkistoaineisto'


class LifecycleEvent(models.Model):
    school = models.ForeignKey('School', db_column='koulun_id')
    lifecycleeventtype = models.ForeignKey('LifecycleEventType', db_column='elikaaritapahtuman_lajin_id')
    day = models.IntegerField(blank=True, null=True, db_column='paiva')
    month = models.IntegerField(blank=True, null=True, db_column='kuukausi')
    year = models.IntegerField(db_column='vuosi')
    decisionmaker = models.CharField(max_length=510, blank=True, db_column='paatoksen_tekija')
    decision_day = models.IntegerField(blank=True, null=True, db_column='paatoksen_paiva')
    decision_month = models.IntegerField(blank=True, null=True, db_column='paatoksen_kuukausi')
    decision_year = models.IntegerField(blank=True, null=True, db_column='paatoksen_vuosi')
    lis_tietoja = models.CharField(db_column='lis\xe4tietoja', max_length=510, blank=True)
    reference = models.CharField(max_length=510, blank=True, db_column='viite')
    approx = models.BooleanField(db_column='noin')

    class Meta:
        managed = False
        db_table = 'Elinkaaritapahtuma'


class LifecycleEventType(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    description = models.CharField(max_length=510, blank=True, db_column='selite')

    class Meta:
        managed = False
        db_table = 'Elinkaaritapahtuman_laji'


class Jatkumo(models.Model):
    koulun_a = models.ForeignKey('School', db_column='koulun_a_id', related_name='jatkumo_a')
    description = models.CharField(max_length=510, blank=True, db_column='selite')
    koulun_b = models.ForeignKey('School', db_column='koulun_b_id', related_name='jatkumo_b')
    day = models.IntegerField(blank=True, null=True, db_column='paiva')
    month = models.IntegerField(blank=True, null=True, db_column='kuukausi')
    year = models.IntegerField(blank=True, null=True, db_column='vuosi')
    reference = models.CharField(max_length=510, blank=True, db_column='viite')
    approx = models.BooleanField(db_column='noin')

    class Meta:
        managed = False
        db_table = 'Jatkumo'


class Neighborhood(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    kaupunginosan_nimi = models.CharField(max_length=510, blank=True, db_column='kaupunginosan_nimi')
    liittamispaiva = models.IntegerField(blank=True, null=True, db_column='liittamispaiva')
    liittamiskuukausi = models.IntegerField(blank=True, null=True, db_column='liittamiskuukausi')
    liittamisvuosi = models.IntegerField(blank=True, null=True, db_column='liittamisvuosi')

    class Meta:
        managed = False
        db_table = 'Kaupunginosa'


class Language(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    kielen_nimi = models.CharField(max_length=510, blank=True, db_column='kielen_nimi')

    class Meta:
        managed = False
        db_table = 'Kieli'


class School(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    erityispiirteet = models.TextField(blank=True, db_column='erityispiirteet')
    sota_ajan_koulu = models.BooleanField(db_column='sota_ajan_koulu')
    lempinimet = models.CharField(max_length=510, blank=True, db_column='lempinimet')
    tarkastettu = models.BooleanField(db_column='tarkastettu')

    class Meta:
        managed = False
        db_table = 'Koulu'


class KoulunAla(models.Model):
    school = models.ForeignKey(School, db_column='koulun_id', related_name='fields')
    field = models.ForeignKey(Field, db_column='alan_id')
    main_school = models.ForeignKey(School, db_column='paakoulun_id', related_name='fields_main')
    begin_day = models.IntegerField(blank=True, null=True, db_column='alkamispaiva')
    begin_month = models.IntegerField(blank=True, null=True, db_column='alkamiskuukausi')
    begin_year = models.IntegerField(blank=True, null=True, db_column='alkamisvuosi')
    approx_begin = models.BooleanField(db_column='noin_a')
    end_day = models.IntegerField(blank=True, null=True, db_column='paattymispaiva')
    end_month = models.IntegerField(blank=True, null=True, db_column='paattymiskuukausi')
    end_year = models.IntegerField(blank=True, null=True, db_column='paattymisvuosi')
    approx_end = models.BooleanField(db_column='noin_p')
    reference = models.CharField(max_length=510, blank=True, db_column='viite')

    class Meta:
        managed = False
        db_table = 'Koulun_ala'


class SchoolLanguage(models.Model):
    school = models.ForeignKey(School, db_column='koulun_id')
    language = models.ForeignKey(Language, db_column='kielen_id')
    begin_year = models.IntegerField(blank=True, null=True, db_column='alkamisvuosi')
    end_year = models.IntegerField(blank=True, null=True, db_column='paattymisvuosi')
    reference = models.CharField(max_length=510, blank=True, db_column='viite')
    approx_begin = models.BooleanField(db_column='noin_a')
    approx_end = models.BooleanField(db_column='noin_p')

    class Meta:
        managed = False
        db_table = 'Koulun_kieli'


class KoulunLaatu(models.Model):
    school = models.ForeignKey(School, db_column='koulun_id')
    schooltype = models.ForeignKey('SchoolType', db_column='koulutyypin_id')
    school = models.ForeignKey(School, db_column='paakoulun_id')
    begin_day = models.IntegerField(blank=True, null=True, db_column='alkamispaiva')
    begin_month = models.IntegerField(blank=True, null=True, db_column='alkamiskuukausi')
    begin_year = models.IntegerField(blank=True, null=True, db_column='alkamisvuosi')
    end_day = models.IntegerField(blank=True, null=True, db_column='paattymispaiva')
    end_month = models.IntegerField(blank=True, null=True, db_column='paattymiskuukausi')
    end_year = models.IntegerField(blank=True, null=True, db_column='paattymisvuosi')
    reference = models.CharField(max_length=510, blank=True, db_column='viite')
    approx_begin = models.BooleanField(db_column='noin_a')
    approx_end = models.BooleanField(db_column='noin_p')

    class Meta:
        managed = False
        db_table = 'Koulun_laatu'


class SchoolOwnership(models.Model):
    school = models.ForeignKey(School, db_column='koulun_id')
    owner_founder = models.ForeignKey('OwnerFounder', db_column='omistaja_perustajan_id')
    begin_day = models.IntegerField(blank=True, null=True, db_column='alkamispaiva')
    begin_month = models.IntegerField(blank=True, null=True, db_column='alkamiskuukausi')
    begin_year = models.IntegerField(blank=True, null=True, db_column='alkamisvuosi')
    end_day = models.IntegerField(blank=True, null=True, db_column='paattymispaiva')
    end_month = models.IntegerField(blank=True, null=True, db_column='paattymiskuukausi')
    end_year = models.IntegerField(blank=True, null=True, db_column='paattymisvuosi')
    reference = models.CharField(max_length=510, blank=True, db_column='viite')
    approx_begin = models.BooleanField(db_column='noin_a')
    approx_end = models.BooleanField(db_column='noin_p')

    class Meta:
        managed = False
        db_table = 'Koulun_omistussuhde'


class SchoolFounder(models.Model):
    school = models.ForeignKey(School, db_column='koulun_id')
    owner_founder = models.ForeignKey('OwnerFounder', db_column='omistaja_perustajan_id')
    reference = models.CharField(max_length=510, blank=True, db_column='viite')

    class Meta:
        managed = False
        db_table = 'Koulun_perustajat'


class SchoolGender(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    school = models.ForeignKey(School, blank=True, null=True, db_column='koulun_id')
    gender = models.CharField(max_length=510, blank=True, db_column='sukupuoli')
    begin_day = models.IntegerField(blank=True, null=True, db_column='alkamispaiva')
    begin_month = models.IntegerField(blank=True, null=True, db_column='alkamiskuukausi')
    begin_year = models.IntegerField(blank=True, null=True, db_column='alkamisvuosi')
    end_day = models.IntegerField(blank=True, null=True, db_column='paattymispaiva')
    end_month = models.IntegerField(blank=True, null=True, db_column='paattymiskuukausi')
    end_year = models.IntegerField(blank=True, null=True, db_column='paattymisvuosi')
    reference = models.CharField(max_length=510, blank=True, db_column='viite')
    approx_begin = models.BooleanField(db_column='noin_a')
    approx_end = models.BooleanField(db_column='noin_p')

    class Meta:
        managed = False
        db_table = 'Koulun_sukupuoli'


class SchoolType(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    type_name = models.CharField(max_length=510, blank=True, db_column='selite')
    description = models.CharField(db_column='mit\xe4_se_tarkoittaa', max_length=510, blank=True)

    class Meta:
        managed = False
        db_table = 'Koulutyyppi'


class LuokkaAsteidenLukumaara(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    school = models.ForeignKey(School, blank=True, null=True, db_column='koulun_id')
    lukumaara = models.IntegerField(blank=True, null=True, db_column='lukumaara')
    begin_day = models.IntegerField(blank=True, null=True, db_column='alkamispaiva')
    begin_month = models.IntegerField(blank=True, null=True, db_column='alkamiskuukausi')
    begin_year = models.IntegerField(blank=True, null=True, db_column='alkamisvuosi')
    end_day = models.IntegerField(blank=True, null=True, db_column='paattymispaiva')
    end_month = models.IntegerField(blank=True, null=True, db_column='paattymiskuukausi')
    end_year = models.IntegerField(blank=True, null=True, db_column='paattymisvuosi')
    reference = models.CharField(max_length=510, blank=True, db_column='viite')
    approx_begin = models.BooleanField(db_column='noin_a')
    approx_end = models.BooleanField(db_column='noin_p')

    class Meta:
        managed = False
        db_table = 'Luokka-asteiden_lukumaara'


class NameType(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    name = models.ForeignKey('SchoolName', blank=True, null=True, related_name='types', db_column='nimen_id')
    type = models.CharField(max_length=510, blank=True, db_column='nimen_tyyppi')
    value = models.CharField(max_length=510, blank=True, db_column='nimi')

    class Meta:
        managed = False
        db_table = 'Nimen_tyyppi'


class SchoolName(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    school = models.ForeignKey(School, blank=True, null=True, related_name='names', db_column='koulun_id')
    begin_day = models.IntegerField(blank=True, null=True, db_column='alkamispaiva')
    begin_month = models.IntegerField(blank=True, null=True, db_column='alkamiskuukausi')
    begin_year = models.IntegerField(blank=True, null=True, db_column='alkamisvuosi')
    end_day = models.IntegerField(blank=True, null=True, db_column='paattymispaiva')
    end_month = models.IntegerField(blank=True, null=True, db_column='paattymiskuukausi')
    end_year = models.IntegerField(blank=True, null=True, db_column='paattymisvuosi')
    reference = models.CharField(max_length=510, blank=True, db_column='viite')
    approx_begin = models.BooleanField(db_column='noin_a')
    approx_end = models.BooleanField(db_column='noin_p')

    class Meta:
        managed = False
        db_table = 'Nimi'


class OwnerFounder(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    name = models.CharField(max_length=510, blank=True, db_column='nimi')
    owner_foundertype = models.ForeignKey('OwnerFounderType', blank=True, null=True,
                                         db_column='omistaja_perustajatyypin_id')

    class Meta:
        managed = False
        db_table = 'Omistaja_Perustaja'


class OwnerFounderType(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    description = models.CharField(max_length=510, blank=True, db_column='selite')

    class Meta:
        managed = False
        db_table = 'Omistaja_Perustajatyyppi'


class Address(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    street_name_fi = models.CharField(max_length=510, blank=True, db_column='kadun_nimi_suomeksi')
    street_name_sv = models.CharField(max_length=510, blank=True, db_column='kadun_nimi_ruotsiksi')
    zip_code = models.CharField(max_length=510, blank=True, db_column='postitoimipaikka')
    municipality_fi = models.CharField(max_length=510, blank=True, db_column='kunnan_nimi_suomeksi')
    municipality_sv = models.CharField(max_length=510, blank=True, db_column='kunnan_nimi_ruotsiksi')
    begin_day = models.IntegerField(blank=True, null=True, db_column='alkamispaiva')
    begin_month = models.IntegerField(blank=True, null=True, db_column='alkamiskuukausi')
    begin_year = models.IntegerField(blank=True, null=True, db_column='alkamisvuosi')
    end_day = models.IntegerField(blank=True, null=True, db_column='paattymispaiva')
    end_month = models.IntegerField(blank=True, null=True, db_column='paattymiskuukausi')
    end_year = models.IntegerField(blank=True, null=True, db_column='paattymisvuosi')
    comment = models.CharField(max_length=510, blank=True, db_column='kommentti')
    approx_begin = models.BooleanField(db_column='noin_a')
    approx_end = models.BooleanField(db_column='noin_p')

    class Meta:
        managed = False
        db_table = 'Osoite'


class BuildingName(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    name = models.CharField(max_length=510, blank=True, db_column='nimi')
    building = models.ForeignKey('Building', blank=True, null=True, db_column='rakennuksen_id')
    begin_year = models.IntegerField(blank=True, null=True, db_column='alkamisvuosi')
    end_year = models.IntegerField(blank=True, null=True, db_column='paattymisvuosi')
    reference = models.CharField(max_length=510, blank=True, db_column='viite')
    approx_begin = models.BooleanField(db_column='noin_a')
    approx_end = models.BooleanField(db_column='noin_p')

    class Meta:
        managed = False
        db_table = 'Rakennuksen_nimi'


class BuildingOwnership(models.Model):
    building = models.ForeignKey('Building', db_column='rakennuksen_id')
    owner_founder = models.ForeignKey(OwnerFounder, db_column='omistaja_perustajan_id')
    begin_day = models.IntegerField(blank=True, null=True, db_column='alkamispaiva')
    begin_month = models.IntegerField(blank=True, null=True, db_column='alkamiskuukausi')
    begin_year = models.IntegerField(blank=True, null=True, db_column='alkamisvuosi')
    end_day = models.IntegerField(blank=True, null=True, db_column='paattymispaiva')
    end_month = models.IntegerField(blank=True, null=True, db_column='paattymiskuukausi')
    end_year = models.IntegerField(blank=True, null=True, db_column='paattymisvuosi')
    reference = models.CharField(max_length=510, blank=True, db_column='viite')
    approx_begin = models.BooleanField(db_column='noin_a')
    approx_end = models.BooleanField(db_column='noin_p')

    class Meta:
        managed = False
        db_table = 'Rakennuksen_omistussuhde'


class BuildingAddress(models.Model):
    building = models.ForeignKey('Building', db_column='rakennuksen_id')
    address = models.ForeignKey(Address, db_column='osoitteen_id')

    class Meta:
        managed = False
        db_table = 'Rakennuksen_osoite'


class BuildingStatus(models.Model):
    school = models.ForeignKey(School, db_column='koulun_id')
    building = models.ForeignKey('Building', db_column='rakennuksen_id')
    ownership = models.BooleanField(db_column='omistus')
    begin_day = models.IntegerField(blank=True, null=True, db_column='alkamispaiva')
    begin_month = models.IntegerField(blank=True, null=True, db_column='alkamiskuukausi')
    begin_year = models.IntegerField(blank=True, null=True, db_column='alkamisvuosi')
    end_day = models.IntegerField(blank=True, null=True, db_column='paattymispaiva')
    end_month = models.IntegerField(blank=True, null=True, db_column='paattymiskuukausi')
    end_year = models.IntegerField(blank=True, null=True, db_column='paattymisvuosi')
    reference = models.CharField(max_length=510, blank=True, db_column='viite')
    approx_begin = models.BooleanField(db_column='noin_a')
    approx_end = models.BooleanField(db_column='noin_p')

    class Meta:
        managed = False
        db_table = 'Rakennuksen_status'


class Building(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    neighborhood = models.ForeignKey(Neighborhood, blank=True, null=True, db_column='kaupunginosan_id')
    rakennusvuosi = models.IntegerField(blank=True, null=True, db_column='rakennusvuosi')
    architect = models.CharField(max_length=510, blank=True, db_column='arkkitehti')
    arkkitehtitoimisto = models.CharField(max_length=510, blank=True, db_column='arkkitehtitoimisto')
    kiinteistonumero = models.CharField(max_length=510, blank=True, db_column='kiinteistonumero')
    kuva = models.BinaryField(blank=True, null=True, db_column='kuva')
    viipalerakennus = models.BooleanField(db_column='viipalerakennus')
    comment = models.CharField(max_length=510, blank=True, db_column='kommentti')
    reference = models.CharField(max_length=510, blank=True, db_column='viite')
    approx = models.BooleanField(db_column='noin')

    class Meta:
        managed = False
        db_table = 'Rakennus'


class Principal(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    surname = models.CharField(max_length=510, blank=True, db_column='sukunimi')
    first_name = models.CharField(max_length=510, blank=True, db_column='etunimi')

    class Meta:
        managed = False
        db_table = 'Rehtori'


class Employership(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    school = models.ForeignKey(School, blank=True, null=True, db_column='koulun_id')
    nimen_id = models.IntegerField(blank=True, null=True, db_column='nimen_id')
    principal = models.ForeignKey(Principal, blank=True, null=True, db_column='rehtorin_id')
    begin_day = models.IntegerField(blank=True, null=True, db_column='alkamispaiva')
    begin_month = models.IntegerField(blank=True, null=True, db_column='alkamiskuukausi')
    begin_year = models.IntegerField(blank=True, null=True, db_column='alkamisvuosi')
    end_day = models.IntegerField(blank=True, null=True, db_column='paattymispaiva')
    end_month = models.IntegerField(blank=True, null=True, db_column='paattymiskuukausi')
    end_year = models.IntegerField(blank=True, null=True, db_column='paattymisvuosi')
    reference = models.CharField(max_length=510, blank=True, db_column='viite')
    approx_begin = models.BooleanField(db_column='noin_a')
    approx_end = models.BooleanField(db_column='noin_p')

    class Meta:
        managed = False
        db_table = 'Tyosuhde'
