# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0007_auto_20150528_1017'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchiveDataLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('archivedata', models.OneToOneField(to='schools.ArchiveData', related_name='link')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
