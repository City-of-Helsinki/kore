# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolBuildingPhoto',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('is_front', models.BooleanField(default=False)),
                ('school_building', models.ForeignKey(to='schools.SchoolBuilding')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
