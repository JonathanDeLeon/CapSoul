# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-29 20:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0024_auto_20171128_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='cid',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='cid_of_media', to='database.Capsule'),
        ),
    ]
