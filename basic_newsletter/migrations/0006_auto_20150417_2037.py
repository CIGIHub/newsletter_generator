# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_newsletter', '0005_auto_20150320_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='drupal_create_script',
            field=models.CharField(blank=True, max_length=1024, null=True, choices=[('/Users/natashascott/Development/cigi_toolkit/scripts/create_cigi_newsletter_node.php.template', 'create_cigi_newsletter_node.php.template'), ('/Users/natashascott/Development/cigi_toolkit/scripts/upload_to_cigi_live.sh', 'upload_to_cigi_live.sh'), ('/Users/natashascott/Development/cigi_toolkit/scripts/upload_to_cigi_staging.sh', 'upload_to_cigi_staging.sh')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='short_title',
            field=models.CharField(max_length=1024, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='upload_script',
            field=models.CharField(blank=True, max_length=1024, null=True, choices=[('/Users/natashascott/Development/cigi_toolkit/scripts/create_cigi_newsletter_node.php.template', 'create_cigi_newsletter_node.php.template'), ('/Users/natashascott/Development/cigi_toolkit/scripts/upload_to_cigi_live.sh', 'upload_to_cigi_live.sh'), ('/Users/natashascott/Development/cigi_toolkit/scripts/upload_to_cigi_staging.sh', 'upload_to_cigi_staging.sh')]),
            preserve_default=True,
        ),
    ]
