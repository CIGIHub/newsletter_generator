# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import basic_newsletter.models
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('icontact', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureType',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('display_title', models.CharField(max_length=255)),
                ('max_title_length', models.IntegerField()),
                ('max_description_length', models.IntegerField()),
                ('display_image', models.BooleanField(default=True)),
                ('image_required', models.BooleanField(default=False)),
                ('max_image_width', models.IntegerField(null=True, blank=True)),
                ('max_image_height', models.IntegerField(null=True, blank=True)),
                ('is_headline', models.BooleanField(default=False)),
                ('weight', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('published_date', models.DateField(null=True, blank=True)),
                ('issue_date', models.DateField(null=True, blank=True)),
                ('published_state', models.CharField(default='Draft', choices=[('Draft', 'Draft'), ('Ready to Test', 'Ready to Test'), ('Published', 'Published')], max_length=25)),
                ('message', models.ForeignKey(to='icontact.Message', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NewsItem',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', ckeditor.fields.RichTextField(default='', blank=True, max_length=200)),
                ('url', models.URLField(verbose_name='Link to story', default='', blank=True)),
                ('description', ckeditor.fields.RichTextField(blank=True, default='')),
                ('by_line', models.CharField(default='', blank=True, max_length=200)),
                ('image', models.ImageField(null=True, blank=True, upload_to=basic_newsletter.models.get_upload_folder)),
                ('scaled_image', models.ImageField(null=True, blank=True, upload_to=basic_newsletter.models.get_upload_folder)),
                ('weight', models.IntegerField(blank=True, default=0)),
                ('feature_type', models.ForeignKey(to='basic_newsletter.FeatureType')),
                ('issue', models.ForeignKey(to='basic_newsletter.Issue')),
            ],
            options={
                'ordering': ('weight',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('short_title', models.CharField(blank=True, max_length=50)),
                ('editor', models.CharField(null=True, blank=True, max_length=50)),
                ('editor_twitter', models.CharField(null=True, blank=True, max_length=25)),
                ('tagline', models.CharField(null=True, blank=True, max_length=200)),
                ('upload_script', models.CharField(null=True, blank=True, choices=[('/Users/csimpson/Development/Projects/Newsletter/newsletter_generator/scripts/create_cigi_newsletter_node.php.template', 'create_cigi_newsletter_node.php.template'), ('/Users/csimpson/Development/Projects/Newsletter/newsletter_generator/scripts/upload_to_cigi_live.sh', 'upload_to_cigi_live.sh'), ('/Users/csimpson/Development/Projects/Newsletter/newsletter_generator/scripts/upload_to_cigi_staging.sh', 'upload_to_cigi_staging.sh')], max_length=1024)),
                ('drupal_create_script', models.CharField(null=True, blank=True, choices=[('/Users/csimpson/Development/Projects/Newsletter/newsletter_generator/scripts/create_cigi_newsletter_node.php.template', 'create_cigi_newsletter_node.php.template'), ('/Users/csimpson/Development/Projects/Newsletter/newsletter_generator/scripts/upload_to_cigi_live.sh', 'upload_to_cigi_live.sh'), ('/Users/csimpson/Development/Projects/Newsletter/newsletter_generator/scripts/upload_to_cigi_staging.sh', 'upload_to_cigi_staging.sh')], max_length=1024)),
                ('associated_list', models.ForeignKey(to='icontact.List', null=True, blank=True)),
                ('campaign', models.ForeignKey(to='icontact.Campaign', null=True, blank=True)),
                ('sender_account', models.ForeignKey(to='icontact.Account', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('filepath', models.CharField(max_length=50)),
                ('plain_text_filepath', models.CharField(null=True, blank=True, max_length=50)),
                ('subject_filepath', models.CharField(null=True, blank=True, max_length=50)),
                ('supported_feature_types', models.ManyToManyField(null=True, to='basic_newsletter.FeatureType', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TemplateAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('value', models.TextField()),
                ('template', models.ForeignKey(to='basic_newsletter.Template')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TemplateMediaFile',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(null=True, blank=True, upload_to=basic_newsletter.models.get_template_upload_folder)),
                ('template', models.ForeignKey(to='basic_newsletter.Template')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='template',
            field=models.ForeignKey(to='basic_newsletter.Template'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='newsletter',
            field=models.ForeignKey(null=True, to='basic_newsletter.Newsletter'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='story_categories',
            field=models.ManyToManyField(null=True, to='basic_newsletter.FeatureType', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='template',
            field=models.ForeignKey(to='basic_newsletter.Template', null=True, blank=True),
            preserve_default=True,
        ),
    ]
