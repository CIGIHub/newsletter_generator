# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_newsletter', '0006_auto_20150417_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='drupal_create_script',
            field=models.CharField(blank=True, max_length=1024, null=True, choices=[('/Users/csimpson/Development/Projects/CIGI/toolkit/scripts/create_cigi_newsletter_node.php.template', 'create_cigi_newsletter_node.php.template'), ('/Users/csimpson/Development/Projects/CIGI/toolkit/scripts/temp.html', 'temp.html'), ('/Users/csimpson/Development/Projects/CIGI/toolkit/scripts/upload_to_ap_staging.sh', 'upload_to_ap_staging.sh'), ('/Users/csimpson/Development/Projects/CIGI/toolkit/scripts/upload_to_cigi_live.sh', 'upload_to_cigi_live.sh'), ('/Users/csimpson/Development/Projects/CIGI/toolkit/scripts/upload_to_cigi_staging.sh', 'upload_to_cigi_staging.sh')]),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='upload_script',
            field=models.CharField(blank=True, max_length=1024, null=True, choices=[('/Users/csimpson/Development/Projects/CIGI/toolkit/scripts/create_cigi_newsletter_node.php.template', 'create_cigi_newsletter_node.php.template'), ('/Users/csimpson/Development/Projects/CIGI/toolkit/scripts/temp.html', 'temp.html'), ('/Users/csimpson/Development/Projects/CIGI/toolkit/scripts/upload_to_ap_staging.sh', 'upload_to_ap_staging.sh'), ('/Users/csimpson/Development/Projects/CIGI/toolkit/scripts/upload_to_cigi_live.sh', 'upload_to_cigi_live.sh'), ('/Users/csimpson/Development/Projects/CIGI/toolkit/scripts/upload_to_cigi_staging.sh', 'upload_to_cigi_staging.sh')]),
        ),
    ]
