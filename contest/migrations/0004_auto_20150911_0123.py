# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0003_auto_20150911_0053'),
    ]

    operations = [
        migrations.RenameField(
            model_name='administrator',
            old_name='shaPassword',
            new_name='password',
        ),
        migrations.AddField(
            model_name='administrator',
            name='username',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
