# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0009_auto_20150918_0445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='image',
            field=models.FileField(upload_to='banners/', null=True),
        ),
    ]
