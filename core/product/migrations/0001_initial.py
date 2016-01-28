# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attribute', '0001_initial'),
        ('category', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('short_description', models.TextField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('slug', models.SlugField(unique=True)),
                ('active', models.BooleanField(default=False)),
                ('attributes', models.ManyToManyField(to='attribute.Attribute')),
                ('category', models.ForeignKey(to='category.Category', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'products')),
                ('alt', models.CharField(max_length=50, null=True, blank=True)),
                ('featured', models.BooleanField(default=False)),
                ('product', models.ForeignKey(to='product.Product')),
            ],
        ),
    ]
