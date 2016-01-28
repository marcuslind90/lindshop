# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0001_initial'),
        ('cart', '0001_initial'),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notification_type', models.CharField(max_length=20, choices=[(b'shipping', b'Shipping'), (b'note', b'Note')])),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('note', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payment_status', models.CharField(default=b'unpaid', max_length=20, choices=[(b'paid', b'Paid'), (b'unpaid', b'Unpaid')])),
                ('payment_option', models.CharField(default=b'unknown', max_length=100)),
                ('subscription', models.BooleanField(default=False)),
                ('subscription_status', models.CharField(blank=True, max_length=20, null=True, choices=[(b'active', b'Active'), (b'unpaid', b'Unpaid'), (b'canceled', b'Canceled')])),
                ('subscription_enddate', models.DateField(null=True, blank=True)),
                ('payment_reference', models.CharField(max_length=200, null=True, blank=True)),
                ('payment_id', models.CharField(max_length=200, null=True, blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('cart', models.ForeignKey(to='cart.Cart')),
                ('customer', models.ForeignKey(to='customer.Customer')),
                ('subscription_plan', models.ForeignKey(blank=True, to='subscription.Plan', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='notification',
            name='order',
            field=models.ForeignKey(to='order.Order'),
        ),
    ]
