# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('basic_newsletter', '0004_auto_20150318_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsitem',
            name='by_line',
            field=models.CharField(max_length=1024, null=True, default='', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newsitem',
            name='description',
            field=ckeditor.fields.RichTextField(null=True, default='', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newsitem',
            name='title',
            field=ckeditor.fields.RichTextField(max_length=1024, null=True, default='', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newsitem',
            name='url',
            field=models.URLField(verbose_name='Link to story', null=True, default='', blank=True),
            preserve_default=True,
        ),
    ]
