# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0002_schoolbuildingphoto'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressLocation',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('address', models.OneToOneField(to='schools.Address', related_name='locations')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='schoolbuilding',
            options={'managed': False, 'ordering': ['school']},
        ),
        migrations.AlterField(
            model_name='schoolbuildingphoto',
            name='is_front',
            field=models.BooleanField(default=True, help_text='Is this a picture of the building front?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='schoolbuildingphoto',
            name='school_building',
            field=models.ForeignKey(to='schools.SchoolBuilding', related_name='photos'),
            preserve_default=True,
        ),
    ]
