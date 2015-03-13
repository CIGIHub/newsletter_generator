# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_newsletter', '0002_auto_20150312_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='name',
            field=models.CharField(max_length=100, default='Template'),
            preserve_default=False,
        ),
    ]
