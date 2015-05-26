# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0004_auto_20150525_0825'),
    ]

    operations = [
        migrations.AddField(
            model_name='addresslocation',
            name='handmade',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
