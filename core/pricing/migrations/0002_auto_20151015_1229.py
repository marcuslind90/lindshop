# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currency',
            name='name',
        ),
        migrations.AddField(
            model_name='currency',
            name='iso_code',
            field=models.CharField(default='THB', max_length=3),
            preserve_default=False,
        ),
    ]
