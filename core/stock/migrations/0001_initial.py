# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stock', models.IntegerField()),
                ('product', models.ForeignKey(to='product.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Default', unique=True, max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='stock',
            name='warehouse',
            field=models.ForeignKey(to='stock.Warehouse'),
        ),
    ]
