# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_newsletter', '0003_template_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleAnalyticsCampaign',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('source', models.CharField(max_length=1024)),
                ('medium', models.CharField(max_length=1024)),
                ('campaign', models.CharField(max_length=1024)),
                ('newsletter', models.ForeignKey(to='basic_newsletter.Newsletter')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='drupal_create_script',
            field=models.CharField(max_length=1024, blank=True, null=True, choices=[('/Users/csimpson/Development/Projects/CIGI/toolkit/scripts/create_cigi_newsletter_node.php.template', 'create_cigi_newsletter_node.php.template'), ('/Users/csimpson/Development/Projects/CIGI/toolkit/scripts/upload_to_cigi_live.sh', 'upload_to_cigi_live.sh'), ('/Users/csimpson/Development/Projects/CIGI/toolkit/scripts/upload_to_cigi_staging.sh', 'upload_to_cigi_staging.sh')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='upload_script',
            field=models.CharField(max_length=1024, blank=True, null=True, choices=[('/Users/csimpson/Development/Projects/CIGI/toolkit/scripts/create_cigi_newsletter_node.php.template', 'create_cigi_newsletter_node.php.template'), ('/Users/csimpson/Development/Projects/CIGI/toolkit/scripts/upload_to_cigi_live.sh', 'upload_to_cigi_live.sh'), ('/Users/csimpson/Development/Projects/CIGI/toolkit/scripts/upload_to_cigi_staging.sh', 'upload_to_cigi_staging.sh')]),
            preserve_default=True,
        ),
    ]
