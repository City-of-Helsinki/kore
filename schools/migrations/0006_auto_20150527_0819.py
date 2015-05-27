# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0005_addresslocation_handmade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addresslocation',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True),
            preserve_default=True,
        ),
    ]
