# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-28 01:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0018_remove_media_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='capsule',
            name='date_created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
