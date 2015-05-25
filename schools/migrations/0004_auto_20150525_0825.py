# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0003_auto_20150520_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addresslocation',
            name='address',
            field=models.OneToOneField(related_name='location', to='schools.Address'),
            preserve_default=True,
        ),
    ]
