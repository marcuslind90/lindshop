# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0001_initial'),
        ('cart', '0003_auto_20151014_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='currency',
            field=models.ForeignKey(default=1, to='pricing.Currency'),
            preserve_default=False,
        ),
    ]
