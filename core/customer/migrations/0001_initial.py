# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=128, null=True, blank=True)),
                ('zipcode', models.CharField(max_length=10, null=True, blank=True)),
                ('city', models.CharField(max_length=100, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('default', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100, null=True, blank=True)),
                ('last_name', models.CharField(max_length=100, null=True, blank=True)),
                ('dog_name', models.CharField(max_length=100, null=True, blank=True)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('phone', models.CharField(max_length=50, null=True, blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('key', models.CharField(max_length=32, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='address',
            name='country',
            field=models.ForeignKey(blank=True, to='customer.Country', null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='customer',
            field=models.ForeignKey(to='customer.Customer'),
        ),
    ]
