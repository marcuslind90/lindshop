# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-15 05:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_category_parent'),
        ('product', '0003_auto_20151012_1337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(null=True, to='category.Category'),
        ),
    ]
