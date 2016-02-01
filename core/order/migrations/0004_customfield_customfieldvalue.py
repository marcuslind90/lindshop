# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20151014_1333'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=50)),
                ('mandatory', models.BooleanField(default=False)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='CustomFieldValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=100)),
                ('custom_field', models.ForeignKey(to='order.CustomField')),
                ('order', models.ForeignKey(to='order.Order')),
            ],
        ),
    ]
