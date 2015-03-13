# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('basic_newsletter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featuretype',
            name='display_title',
            field=models.CharField(max_length=1024),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newsitem',
            name='by_line',
            field=models.CharField(default='', blank=True, max_length=1024),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newsitem',
            name='title',
            field=ckeditor.fields.RichTextField(default='', blank=True, max_length=1024),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='tagline',
            field=models.CharField(null=True, blank=True, max_length=1024),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='title',
            field=models.CharField(max_length=1024),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='template',
            name='filepath',
            field=models.CharField(max_length=1024),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='template',
            name='plain_text_filepath',
            field=models.CharField(null=True, blank=True, max_length=1024),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='template',
            name='subject_filepath',
            field=models.CharField(null=True, blank=True, max_length=1024),
            preserve_default=True,
        ),
    ]
