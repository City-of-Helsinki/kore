# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0006_auto_20150527_0819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addresslocation',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, srid=4326, null=True),
            preserve_default=True,
        ),
    ]
