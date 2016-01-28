# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20151014_1315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='email',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='last_name',
        ),
    ]
