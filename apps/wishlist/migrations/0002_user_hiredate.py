# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 23:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='hiredate',
            field=models.DateTimeField(null=True),
        ),
    ]
