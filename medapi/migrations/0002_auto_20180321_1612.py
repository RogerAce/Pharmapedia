# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-21 10:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medapi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bname',
            name='medkey',
        ),
        migrations.RemoveField(
            model_name='gname',
            name='medkey',
        ),
        migrations.DeleteModel(
            name='Bname',
        ),
        migrations.DeleteModel(
            name='Gname',
        ),
        migrations.DeleteModel(
            name='medicine',
        ),
    ]