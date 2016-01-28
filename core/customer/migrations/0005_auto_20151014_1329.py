# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_auto_20151014_1329'),
        ('order', '0002_auto_20151014_1329'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0004_auto_20151014_1316'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dog_name', models.CharField(max_length=100, null=True, blank=True)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('phone', models.CharField(max_length=50, null=True, blank=True)),
                ('key', models.CharField(max_length=32, null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='customer',
            name='user',
        ),
        migrations.RemoveField(
            model_name='address',
            name='customer',
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
