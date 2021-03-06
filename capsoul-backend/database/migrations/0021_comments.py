# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-28 01:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0020_auto_20171127_1741'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('comid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=255)),
                ('text', models.TextField(default='')),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cid_of_comment', to='database.Capsule')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
