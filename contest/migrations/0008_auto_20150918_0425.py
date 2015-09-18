# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0007_auto_20150918_0157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='contest',
            field=models.ForeignKey(to='contest.Contest', null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='created_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='message',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='owner',
            field=models.ForeignKey(to='contest.Competitor', null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='path_original',
            field=models.FileField(upload_to='original_videos/', null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='path_processed',
            field=models.FileField(upload_to='converted_videos/', null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='status',
            field=models.CharField(max_length=1, choices=[('2', 'Ready'), ('1', 'In Process'), ('0', 'Disabled')], null=True, default=0),
        ),
    ]
