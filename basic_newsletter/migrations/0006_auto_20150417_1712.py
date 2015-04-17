# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import basic_newsletter.models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_newsletter', '0005_auto_20150320_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsitem',
            name='image',
            field=models.ImageField(blank=True, null=True, max_length=1024, upload_to=basic_newsletter.models.get_upload_folder),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newsitem',
            name='scaled_image',
            field=models.ImageField(blank=True, null=True, max_length=1024, upload_to=basic_newsletter.models.get_upload_folder),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='drupal_create_script',
            field=models.CharField(blank=True, null=True, max_length=1024, choices=[('/Users/csimpson/Development/Projects/CIGI/toolkit/scripts/create_cigi_newsletter_node.php.template', 'create_cigi_newsletter_node.php.template'), ('/Users/csimpson/Development/Projects/CIGI/toolkit/scripts/temp.html', 'temp.html'), ('/Users/csimpson/Development/Projects/CIGI/toolkit/scripts/upload_to_cigi_live.sh', 'upload_to_cigi_live.sh'), ('/Users/csimpson/Development/Projects/CIGI/toolkit/scripts/upload_to_cigi_staging.sh', 'upload_to_cigi_staging.sh')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='upload_script',
            field=models.CharField(blank=True, null=True, max_length=1024, choices=[('/Users/csimpson/Development/Projects/CIGI/toolkit/scripts/create_cigi_newsletter_node.php.template', 'create_cigi_newsletter_node.php.template'), ('/Users/csimpson/Development/Projects/CIGI/toolkit/scripts/temp.html', 'temp.html'), ('/Users/csimpson/Development/Projects/CIGI/toolkit/scripts/upload_to_cigi_live.sh', 'upload_to_cigi_live.sh'), ('/Users/csimpson/Development/Projects/CIGI/toolkit/scripts/upload_to_cigi_staging.sh', 'upload_to_cigi_staging.sh')]),
            preserve_default=True,
        ),
    ]
