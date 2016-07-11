# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-08 10:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_productdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataPreset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('data', models.ManyToManyField(to='product.ProductData')),
            ],
        ),
    ]
