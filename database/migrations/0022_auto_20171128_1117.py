# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-28 19:17
from __future__ import unicode_literals

import database.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0021_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='file',
            field=models.FileField(upload_to=database.models._upload_path),
        ),
    ]