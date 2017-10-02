# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('street_name_fi', models.CharField(db_column='kadun_nimi_suomeksi', blank=True, max_length=510)),
                ('street_name_sv', models.CharField(db_column='kadun_nimi_ruotsiksi', blank=True, max_length=510)),
                ('zip_code', models.CharField(db_column='postitoimipaikka', blank=True, max_length=510)),
                ('municipality_fi', models.CharField(db_column='kunnan_nimi_suomeksi', blank=True, max_length=510)),
                ('municipality_sv', models.CharField(db_column='kunnan_nimi_ruotsiksi', blank=True, max_length=510)),
                ('begin_day', models.IntegerField(db_column='alkamispaiva', blank=True, null=True)),
                ('begin_month', models.IntegerField(db_column='alkamiskuukausi', blank=True, null=True)),
                ('begin_year', models.IntegerField(db_column='alkamisvuosi', blank=True, null=True)),
                ('end_day', models.IntegerField(db_column='paattymispaiva', blank=True, null=True)),
                ('end_month', models.IntegerField(db_column='paattymiskuukausi', blank=True, null=True)),
                ('end_year', models.IntegerField(db_column='paattymisvuosi', blank=True, null=True)),
                ('comment', models.CharField(db_column='kommentti', blank=True, max_length=510)),
                ('approx_begin', models.BooleanField(db_column='noin_a', default=False)),
                ('approx_end', models.BooleanField(db_column='noin_p', default=False)),
            ],
            options={
                'db_table': 'Osoite',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArchiveData',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('location', models.CharField(db_column='sijainti', blank=True, max_length=510)),
                ('begin_year', models.IntegerField(db_column='alkamisvuosi', blank=True, null=True)),
                ('end_year', models.IntegerField(db_column='paattymisvuosi', blank=True, null=True)),
                ('arkiston_nimi', models.CharField(db_column='arkiston_nimi', blank=True, max_length=510)),
            ],
            options={
                'db_table': 'Arkistoaineisto',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('construction_year', models.IntegerField(db_column='rakennusvuosi', blank=True, null=True)),
                ('architect', models.CharField(db_column='arkkitehti', blank=True, max_length=510)),
                ('architect_firm', models.CharField(db_column='arkkitehtitoimisto', blank=True, max_length=510)),
                ('property_number', models.CharField(db_column='kiinteistonumero', blank=True, max_length=510)),
                ('photo', models.BinaryField(db_column='kuva', blank=True, null=True)),
                ('sliced', models.BooleanField(db_column='viipalerakennus', default=False)),
                ('comment', models.CharField(db_column='kommentti', blank=True, max_length=510)),
                ('reference', models.CharField(db_column='viite', blank=True, max_length=510)),
                ('approx', models.BooleanField(db_column='noin', default=False)),
            ],
            options={
                'db_table': 'Rakennus',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BuildingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
            ],
            options={
                'db_table': 'Rakennuksen_osoite',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BuildingName',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='nimi', blank=True, max_length=510)),
                ('begin_year', models.IntegerField(db_column='alkamisvuosi', blank=True, null=True)),
                ('end_year', models.IntegerField(db_column='paattymisvuosi', blank=True, null=True)),
                ('reference', models.CharField(db_column='viite', blank=True, max_length=510)),
                ('approx_begin', models.BooleanField(db_column='noin_a', default=False)),
                ('approx_end', models.BooleanField(db_column='noin_p', default=False)),
            ],
            options={
                'db_table': 'Rakennuksen_nimi',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BuildingOwnership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('begin_day', models.IntegerField(db_column='alkamispaiva', blank=True, null=True)),
                ('begin_month', models.IntegerField(db_column='alkamiskuukausi', blank=True, null=True)),
                ('begin_year', models.IntegerField(db_column='alkamisvuosi', blank=True, null=True)),
                ('end_day', models.IntegerField(db_column='paattymispaiva', blank=True, null=True)),
                ('end_month', models.IntegerField(db_column='paattymiskuukausi', blank=True, null=True)),
                ('end_year', models.IntegerField(db_column='paattymisvuosi', blank=True, null=True)),
                ('reference', models.CharField(db_column='viite', blank=True, max_length=510)),
                ('approx_begin', models.BooleanField(db_column='noin_a', default=False)),
                ('approx_end', models.BooleanField(db_column='noin_p', default=False)),
            ],
            options={
                'db_table': 'Rakennuksen_omistussuhde',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DataType',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='nimi', blank=True, max_length=510)),
            ],
            options={
                'db_table': 'Aineistotyyppi',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Employership',
            fields=[
                ('id', models.IntegerField(db_column='ID', blank=False, null=False, unique=True, serialize=False)),
                ('nimen_id', models.IntegerField(db_column='nimen_id', blank=True, null=True)),
                ('begin_day', models.IntegerField(db_column='alkamispaiva', blank=True, null=True)),
                ('begin_month', models.IntegerField(db_column='alkamiskuukausi', blank=True, null=True)),
                ('begin_year', models.IntegerField(db_column='alkamisvuosi', blank=True, null=True)),
                ('end_day', models.IntegerField(db_column='paattymispaiva', blank=True, null=True)),
                ('end_month', models.IntegerField(db_column='paattymiskuukausi', blank=True, null=True)),
                ('end_year', models.IntegerField(db_column='paattymisvuosi', blank=True, null=True)),
                ('reference', models.CharField(db_column='viite', blank=True, max_length=510)),
                ('approx_begin', models.BooleanField(db_column='noin_a', default=False)),
                ('approx_end', models.BooleanField(db_column='noin_p', default=False)),
            ],
            options={
                'db_table': 'Tyosuhde',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='kielen_nimi', blank=True, max_length=510)),
            ],
            options={
                'db_table': 'Kieli',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LifecycleEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('day', models.IntegerField(db_column='paiva', blank=True, null=True)),
                ('month', models.IntegerField(db_column='kuukausi', blank=True, null=True)),
                ('year', models.IntegerField(db_column='vuosi')),
                ('decisionmaker', models.CharField(db_column='paatoksen_tekija', blank=True, max_length=510)),
                ('decision_day', models.IntegerField(db_column='paatoksen_paiva', blank=True, null=True)),
                ('decision_month', models.IntegerField(db_column='paatoksen_kuukausi', blank=True, null=True)),
                ('decision_year', models.IntegerField(db_column='paatoksen_vuosi', blank=True, null=True)),
                ('additional_info', models.CharField(db_column='lisätietoja', blank=True, max_length=510)),
                ('reference', models.CharField(db_column='viite', blank=True, max_length=510)),
                ('approx', models.BooleanField(db_column='noin', default=False)),
            ],
            options={
                'db_table': 'Elinkaaritapahtuma',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LifecycleEventType',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('description', models.CharField(db_column='selite', blank=True, max_length=510)),
            ],
            options={
                'db_table': 'Elinkaaritapahtuman_laji',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NameType',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('type', models.CharField(db_column='nimen_tyyppi', blank=True, max_length=510)),
                ('value', models.CharField(db_column='nimi', blank=True, max_length=510)),
            ],
            options={
                'db_table': 'Nimen_tyyppi',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Neighborhood',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='kaupunginosan_nimi', blank=True, max_length=510)),
                ('merge_day', models.IntegerField(db_column='liittamispaiva', blank=True, null=True)),
                ('merge_month', models.IntegerField(db_column='liittamiskuukausi', blank=True, null=True)),
                ('merge_year', models.IntegerField(db_column='liittamisvuosi', blank=True, null=True)),
            ],
            options={
                'db_table': 'Kaupunginosa',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NumberOfGrades',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('number', models.IntegerField(db_column='lukumaara', blank=True, null=True)),
                ('begin_day', models.IntegerField(db_column='alkamispaiva', blank=True, null=True)),
                ('begin_month', models.IntegerField(db_column='alkamiskuukausi', blank=True, null=True)),
                ('begin_year', models.IntegerField(db_column='alkamisvuosi', blank=True, null=True)),
                ('end_day', models.IntegerField(db_column='paattymispaiva', blank=True, null=True)),
                ('end_month', models.IntegerField(db_column='paattymiskuukausi', blank=True, null=True)),
                ('end_year', models.IntegerField(db_column='paattymisvuosi', blank=True, null=True)),
                ('reference', models.CharField(db_column='viite', blank=True, max_length=510)),
                ('approx_begin', models.BooleanField(db_column='noin_a', default=False)),
                ('approx_end', models.BooleanField(db_column='noin_p', default=False)),
            ],
            options={
                'db_table': 'Luokka-asteiden_lukumaara',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OwnerFounder',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='nimi', blank=True, max_length=510)),
            ],
            options={
                'db_table': 'Omistaja_Perustaja',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OwnerFounderType',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('description', models.CharField(db_column='selite', blank=True, max_length=510)),
            ],
            options={
                'db_table': 'Omistaja_Perustajatyyppi',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Principal',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('surname', models.CharField(db_column='sukunimi', blank=True, max_length=510)),
                ('first_name', models.CharField(db_column='etunimi', blank=True, max_length=510)),
            ],
            options={
                'db_table': 'Rehtori',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('special_features', models.TextField(db_column='erityispiirteet', blank=True)),
                ('wartime_school', models.BooleanField(db_column='sota_ajan_koulu', default=False)),
                ('nicknames', models.CharField(db_column='lempinimet', blank=True, max_length=510)),
                ('checked', models.BooleanField(db_column='tarkastettu', default=False)),
            ],
            options={
                'db_table': 'Koulu',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SchoolBuilding',
            fields=[
                ('id', models.CharField(serialize=False, primary_key=True, max_length=100)),
                ('ownership', models.BooleanField(db_column='omistus', default=False)),
                ('begin_day', models.IntegerField(db_column='alkamispaiva', blank=True, null=True)),
                ('begin_month', models.IntegerField(db_column='alkamiskuukausi', blank=True, null=True)),
                ('begin_year', models.IntegerField(db_column='alkamisvuosi', blank=True, null=True)),
                ('end_day', models.IntegerField(db_column='paattymispaiva', blank=True, null=True)),
                ('end_month', models.IntegerField(db_column='paattymiskuukausi', blank=True, null=True)),
                ('end_year', models.IntegerField(db_column='paattymisvuosi', blank=True, null=True)),
                ('reference', models.CharField(db_column='viite', blank=True, max_length=510)),
                ('approx_begin', models.BooleanField(db_column='noin_a', default=False)),
                ('approx_end', models.BooleanField(db_column='noin_p', default=False)),
            ],
            options={
                'db_table': 'Rakennuksen_status',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SchoolContinuum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('description', models.CharField(db_column='selite', blank=True, max_length=510)),
                ('day', models.IntegerField(db_column='paiva', blank=True, null=True)),
                ('month', models.IntegerField(db_column='kuukausi', blank=True, null=True)),
                ('year', models.IntegerField(db_column='vuosi', blank=True, null=True)),
                ('reference', models.CharField(db_column='viite', blank=True, max_length=510)),
                ('approx', models.BooleanField(db_column='noin', default=False)),
            ],
            options={
                'db_table': 'Jatkumo',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SchoolField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('begin_day', models.IntegerField(db_column='alkamispaiva', blank=True, null=True)),
                ('begin_month', models.IntegerField(db_column='alkamiskuukausi', blank=True, null=True)),
                ('begin_year', models.IntegerField(db_column='alkamisvuosi', blank=True, null=True)),
                ('approx_begin', models.BooleanField(db_column='noin_a', default=False)),
                ('end_day', models.IntegerField(db_column='paattymispaiva', blank=True, null=True)),
                ('end_month', models.IntegerField(db_column='paattymiskuukausi', blank=True, null=True)),
                ('end_year', models.IntegerField(db_column='paattymisvuosi', blank=True, null=True)),
                ('approx_end', models.BooleanField(db_column='noin_p', default=False)),
                ('reference', models.CharField(db_column='viite', blank=True, max_length=510)),
            ],
            options={
                'db_table': 'Koulun_ala',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SchoolFieldName',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('description', models.CharField(db_column='selite', blank=True, max_length=510)),
            ],
            options={
                'db_table': 'Ala',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SchoolFounder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('reference', models.CharField(db_column='viite', blank=True, max_length=510)),
            ],
            options={
                'db_table': 'Koulun_perustajat',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SchoolGender',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('gender', models.CharField(db_column='sukupuoli', blank=True, max_length=510)),
                ('begin_day', models.IntegerField(db_column='alkamispaiva', blank=True, null=True)),
                ('begin_month', models.IntegerField(db_column='alkamiskuukausi', blank=True, null=True)),
                ('begin_year', models.IntegerField(db_column='alkamisvuosi', blank=True, null=True)),
                ('end_day', models.IntegerField(db_column='paattymispaiva', blank=True, null=True)),
                ('end_month', models.IntegerField(db_column='paattymiskuukausi', blank=True, null=True)),
                ('end_year', models.IntegerField(db_column='paattymisvuosi', blank=True, null=True)),
                ('reference', models.CharField(db_column='viite', blank=True, max_length=510)),
                ('approx_begin', models.BooleanField(db_column='noin_a', default=False)),
                ('approx_end', models.BooleanField(db_column='noin_p', default=False)),
            ],
            options={
                'db_table': 'Koulun_sukupuoli',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SchoolLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('begin_year', models.IntegerField(db_column='alkamisvuosi', blank=True, null=True)),
                ('end_year', models.IntegerField(db_column='paattymisvuosi', blank=True, null=True)),
                ('reference', models.CharField(db_column='viite', blank=True, max_length=510)),
                ('approx_begin', models.BooleanField(db_column='noin_a', default=False)),
                ('approx_end', models.BooleanField(db_column='noin_p', default=False)),
            ],
            options={
                'db_table': 'Koulun_kieli',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SchoolName',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('begin_day', models.IntegerField(db_column='alkamispaiva', blank=True, null=True)),
                ('begin_month', models.IntegerField(db_column='alkamiskuukausi', blank=True, null=True)),
                ('begin_year', models.IntegerField(db_column='alkamisvuosi', blank=True, null=True)),
                ('end_day', models.IntegerField(db_column='paattymispaiva', blank=True, null=True)),
                ('end_month', models.IntegerField(db_column='paattymiskuukausi', blank=True, null=True)),
                ('end_year', models.IntegerField(db_column='paattymisvuosi', blank=True, null=True)),
                ('reference', models.CharField(db_column='viite', blank=True, max_length=510)),
                ('approx_begin', models.BooleanField(db_column='noin_a', default=False)),
                ('approx_end', models.BooleanField(db_column='noin_p', default=False)),
            ],
            options={
                'db_table': 'Nimi',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SchoolOwnership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('begin_day', models.IntegerField(db_column='alkamispaiva', blank=True, null=True)),
                ('begin_month', models.IntegerField(db_column='alkamiskuukausi', blank=True, null=True)),
                ('begin_year', models.IntegerField(db_column='alkamisvuosi', blank=True, null=True)),
                ('end_day', models.IntegerField(db_column='paattymispaiva', blank=True, null=True)),
                ('end_month', models.IntegerField(db_column='paattymiskuukausi', blank=True, null=True)),
                ('end_year', models.IntegerField(db_column='paattymisvuosi', blank=True, null=True)),
                ('reference', models.CharField(db_column='viite', blank=True, max_length=510)),
                ('approx_begin', models.BooleanField(db_column='noin_a', default=False)),
                ('approx_end', models.BooleanField(db_column='noin_p', default=False)),
            ],
            options={
                'db_table': 'Koulun_omistussuhde',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SchoolType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('begin_day', models.IntegerField(db_column='alkamispaiva', blank=True, null=True)),
                ('begin_month', models.IntegerField(db_column='alkamiskuukausi', blank=True, null=True)),
                ('begin_year', models.IntegerField(db_column='alkamisvuosi', blank=True, null=True)),
                ('end_day', models.IntegerField(db_column='paattymispaiva', blank=True, null=True)),
                ('end_month', models.IntegerField(db_column='paattymiskuukausi', blank=True, null=True)),
                ('end_year', models.IntegerField(db_column='paattymisvuosi', blank=True, null=True)),
                ('reference', models.CharField(db_column='viite', blank=True, max_length=510)),
                ('approx_begin', models.BooleanField(db_column='noin_a', default=False)),
                ('approx_end', models.BooleanField(db_column='noin_p', default=False)),
            ],
            options={
                'db_table': 'Koulun_laatu',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SchoolTypeName',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='selite', blank=True, max_length=510)),
                ('description', models.CharField(db_column='mitä_se_tarkoittaa', blank=True, max_length=510)),
            ],
            options={
                'db_table': 'Koulutyyppi',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
