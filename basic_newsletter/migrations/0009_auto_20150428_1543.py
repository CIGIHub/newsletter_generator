# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_newsletter', '0008_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='story_categories',
            field=models.ManyToManyField(to='basic_newsletter.FeatureType'),
        ),
        migrations.AlterField(
            model_name='template',
            name='supported_feature_types',
            field=models.ManyToManyField(to='basic_newsletter.FeatureType'),
        ),
    ]
