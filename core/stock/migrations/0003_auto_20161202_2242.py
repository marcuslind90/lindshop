# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-02 15:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_auto_20160315_1200'),
        ('stock', '0002_stock_shelf'),
    ]

    operations = [
        migrations.AddField(
            model_name='warehouse',
            name='address',
            field=models.CharField(default='HelloWorld', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='warehouse',
            name='country',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='customer.Country'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='warehouse',
            name='default',
            field=models.BooleanField(default=True),
        ),
    ]