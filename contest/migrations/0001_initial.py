# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('first_name', models.CharField(max_length=512)),
                ('last_name', models.CharField(max_length=512)),
                ('email', models.CharField(max_length=512)),
                ('shaPassword', models.CharField(max_length=512)),
                ('enable', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('choice_text', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=256)),
                ('image', models.CharField(max_length=512)),
                ('url', models.CharField(max_length=512)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('created_date', models.DateTimeField()),
                ('enable', models.BooleanField(default=True)),
                ('prize', models.CharField(max_length=512)),
                ('detail', models.CharField(max_length=512)),
                ('owner', models.ForeignKey(to='contest.Administrator')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('question_text', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_date', models.DateTimeField()),
                ('message', models.CharField(max_length=256)),
                ('status', models.CharField(max_length=1, default=0, choices=[('2', 'Ready'), ('1', 'In Process'), ('0', 'Disabled')])),
                ('path_original', models.CharField(max_length=512)),
                ('path_processed', models.CharField(max_length=512)),
                ('contest', models.ForeignKey(to='contest.Contest')),
            ],
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(to='contest.Question'),
        ),
    ]
