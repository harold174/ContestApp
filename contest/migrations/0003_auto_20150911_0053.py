# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0002_auto_20150910_0609'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('first_name', models.CharField(max_length=256)),
                ('last_name', models.CharField(max_length=256)),
                ('email', models.CharField(max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name='video',
            name='owner',
            field=models.ForeignKey(to='contest.Competitor', default=0),
            preserve_default=False,
        ),
    ]
