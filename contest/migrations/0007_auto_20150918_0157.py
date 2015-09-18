# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0006_profileimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='path_original',
            field=models.FileField(upload_to='original_videos'),
        ),
        migrations.AlterField(
            model_name='video',
            name='path_processed',
            field=models.FileField(upload_to='converted_videos', null=True),
        ),
    ]
