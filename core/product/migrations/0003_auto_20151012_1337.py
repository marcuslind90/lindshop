# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20151009_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='seo_description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='seo_title',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
