# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-08 10:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_datapreset'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DataPreset',
            new_name='ProductDataPreset',
        ),
    ]
