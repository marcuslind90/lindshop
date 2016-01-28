# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10)),
                ('format', models.CharField(max_length=10, null=True, blank=True)),
                ('default', models.BooleanField(default=False)),
                ('language', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('min_amount', models.IntegerField(default=1)),
                ('value', models.FloatField()),
                ('value_type', models.CharField(max_length=20, choices=[(b'percentage', b'Percentage'), (b'value', b'Value')])),
                ('product', models.ForeignKey(to='product.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.FloatField()),
                ('currency', models.ForeignKey(to='pricing.Currency')),
                ('plan', models.ForeignKey(blank=True, to='subscription.Plan', null=True)),
                ('product', models.ForeignKey(blank=True, to='product.Product', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Taxrule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('percentage', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=50)),
                ('value', models.IntegerField()),
                ('value_type', models.CharField(max_length=20, choices=[(b'percentage', b'Percentage'), (b'value', b'Value')])),
            ],
        ),
        migrations.AddField(
            model_name='pricing',
            name='taxrule',
            field=models.ForeignKey(to='pricing.Taxrule'),
        ),
    ]
