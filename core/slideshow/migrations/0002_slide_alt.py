# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-06 09:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slideshow', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='slide',
            name='alt',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
