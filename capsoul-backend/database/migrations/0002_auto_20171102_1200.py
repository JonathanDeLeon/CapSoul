# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-02 19:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='capsule',
            name='comments',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='capsule',
            name='letters',
            field=models.FileField(default='', upload_to=''),
        ),
        migrations.AddField(
            model_name='capsule',
            name='media',
            field=models.FileField(default='', upload_to=''),
        ),
        migrations.AlterField(
            model_name='capsule',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='capsule',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='database.User'),
        ),
        migrations.AlterField(
            model_name='capsule',
            name='title',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='user',
            name='location',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(upload_to=''),
        ),
    ]
