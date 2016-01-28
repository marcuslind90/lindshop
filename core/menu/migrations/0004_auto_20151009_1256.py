# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_auto_20151009_1228'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menuitem',
            old_name='label',
            new_name='custom_label',
        ),
        migrations.RenameField(
            model_name='menuitem',
            old_name='url',
            new_name='custom_url',
        ),
    ]
