# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-23 09:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='option',
            field=models.CharField(default='check', max_length=5),
            preserve_default=False,
        ),
    ]