# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_auto_20151014_1329'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='customer',
            new_name='user',
        ),
    ]
