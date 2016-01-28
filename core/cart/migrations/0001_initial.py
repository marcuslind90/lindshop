# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '__first__'),
        ('subscription', '__first__'),
        ('attribute', '0001_initial'),
        ('shipping', '__first__'),
        ('customer', '__first__'),
        ('pricing', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('carrier', models.ForeignKey(blank=True, to='shipping.Carrier', null=True)),
                ('customer', models.ForeignKey(blank=True, to='customer.Customer', null=True)),
                ('voucher', models.ForeignKey(blank=True, to='pricing.Voucher', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField(default=1)),
                ('attribute', models.ManyToManyField(to='attribute.AttributeChoice')),
                ('cart', models.ForeignKey(to='cart.Cart')),
                ('plan', models.ForeignKey(blank=True, to='subscription.Plan', null=True)),
                ('product', models.ForeignKey(blank=True, to='product.Product', null=True)),
            ],
        ),
    ]
