# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_category_parent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=100, null=True, blank=True)),
                ('url', models.URLField(null=True, blank=True)),
                ('category', models.ForeignKey(blank=True, to='category.Category', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='menu',
            name='items',
            field=models.ManyToManyField(to='menu.MenuItem'),
        ),
    ]
