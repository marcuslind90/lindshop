# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0001_initial'),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('delivery_text', models.CharField(max_length=100)),
                ('logo', models.ImageField(null=True, upload_to=b'carriers', blank=True)),
                ('default', models.BooleanField(default=True)),
                ('countries', models.ManyToManyField(to='customer.Country')),
            ],
        ),
        migrations.CreateModel(
            name='CarrierPricing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.FloatField()),
                ('carrier', models.ForeignKey(to='shipping.Carrier')),
                ('currency', models.ForeignKey(to='pricing.Currency')),
                ('taxrule', models.ForeignKey(to='pricing.Taxrule')),
            ],
        ),
    ]
