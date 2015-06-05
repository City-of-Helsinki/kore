# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0008_archivedatalink'),
    ]

    operations = [
        migrations.RenameField(
            model_name='archivedatalink',
            old_name='archivedata',
            new_name='archive_data',
        ),
    ]
