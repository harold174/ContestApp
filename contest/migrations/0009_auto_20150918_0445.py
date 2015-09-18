# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0008_auto_20150918_0425'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='converter_finish_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='converter_start_date',
            field=models.DateTimeField(null=True),
        ),
    ]
