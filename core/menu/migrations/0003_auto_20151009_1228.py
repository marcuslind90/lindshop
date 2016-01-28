# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_menu_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
