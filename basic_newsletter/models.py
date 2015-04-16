from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.functional import lazy
from ckeditor.fields import RichTextField
from .utils import ImageManipulator
from django.utils.encoding import smart_text
import os
import subprocess
import tempfile


def get_upload_folder(instance, filename):
    return os.path.join(slugify(instance.issue.newsletter.title),
                        str(instance.issue.id), filename)


def get_template_upload_folder(instance, filename):
    return os.path.join(slugify(instance.template.filepath), filename)


def get_scripts():
    scripts_directory = os.path.join(settings.BASE_DIR, 'scripts')
    files = os.listdir(scripts_directory)

    scripts = []
    for script in files:
        scripts.append((os.path.join(scripts_directory, script), script))

    return tuple(scripts)


# Unique newsletter types such as CIGI Worldwide
@python_2_unicode_compatible
class Newsletter(models.Model):
    title = models.CharField(max_length=1024)
    short_title = models.CharField(max_length=50, blank=True)
    editor = models.CharField(max_length=50, null=True, blank=True)
    editor_twitter = models.CharField(max_length=25, null=True, blank=True)
    tagline = models.CharField(max_length=1024, null=True, blank=True)
    template = models.ForeignKey("Template")

    sender_account = models.ForeignKey(settings.MAILER_ACCOUNT_MODEL, null=True, blank=True)
    campaign = models.ForeignKey(settings.MAILER_CAMPAIGN_MODEL, null=True, blank=True)
    associated_list = models.ForeignKey(settings.MAILER_LIST_MODEL, null=True, blank=True)

    upload_script = models.CharField(max_length=1024, null=True, blank=True,
                                     choices=lazy(get_scripts, tuple)())

    drupal_create_script = models.CharField(max_length=1024, null=True,
                                            blank=True,
                                            choices=lazy(get_scripts, tuple)())

    def save(self, *args, **kwargs):
        self.short_title = self.template.filepath[:-5]
        super(Newsletter, self).save(*args,
                                     **kwargs)  # Call the "real" save() method.

    def __str__(self):
        return '%s' % self.title


@python_2_unicode_compatible
class GoogleAnalyticsCampaign(models.Model):
    source = models.CharField(max_length=1024)
    medium = models.CharField(max_length=1024)
    campaign = models.CharField(max_length=1024)

    newsletter = models.ForeignKey("Newsletter")

    @property
    def link_tracking(self):
        return "?utm_source={}&utm_medium={}&utm_campaign={}".format(self.source,
                                                                     self.medium,
                                                                     self.campaign)

    def __str__(self):
        return '{} - {} - {}'.format(self.source, self.medium, self.campaign)


# Specific newsletter issue for a defined newsletter,
# such as December 2013, CIGI Worldwide
# Each issue can be linked to one newsletter type
@python_2_unicode_compatible
class Issue(models.Model):
    PUBLISHED_STATES = (
        ('Draft', 'Draft'),
        ('Ready to Test', 'Ready to Test'),
        ('Published', 'Published'),
    )

    published_date = models.DateField(null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    template = models.ForeignKey("Template", null=True, blank=True)
    newsletter = models.ForeignKey("Newsletter", null=True)
    published_state = models.CharField(default="Draft", max_length=25,
                                       choices=PUBLISHED_STATES)

    message = models.ForeignKey(settings.MAILER_MESSAGE_MODEL, null=True, blank=True)
    story_categories = models.ManyToManyField("FeatureType", null=True,
                                              blank=True)

    @property
    def headline_categories(self):
        return self.story_categories.filter(is_headline=True).order_by(
            "weight")

    @property
    def non_headline_categories(self):
        return self.story_categories.filter(is_headline=False).order_by(
            "weight")

    @property
    def resolved_template(self):
        if self.template:
            return self.template
        else:
            return self.newsletter.template

    @property
    def html_email_template(self):
        if self.template:
            return self.template.filepath
        else:
            return self.newsletter.template.filepath

    @property
    def plain_text_email_template(self):
        if self.template:
            return self.template.plain_text_filepath
        else:
            return self.newsletter.template.plain_text_filepath

    @property
    def subject_template(self):
        if self.template:
            return self.template.subject_filepath
        else:
            return self.newsletter.template.subject_filepath

    @property
    def link_tracking(self):
        ga_campaigns = self.newsletter.googleanalyticscampaign_set.all()

        if len(ga_campaigns) > 0:
            return ga_campaigns[0].link_tracking

        return ""

    def is_complete(self):
        errors = []
        # TODO: use template details to do this generically

        return errors

    def mark_ready_to_publish(self, request=None):
        self.published_state = 'Ready to Test'
        self.save()

    def publish(self, request=None):
        settings.MAILER_UPLOAD_MESSAGE_FUNCTION(self, request)
        self.send(request=request)
        self.upload()
        self.published_state = 'Published'
        self.save()

    def send(self, request=None):
        settings.MAILER_SEND_MESSAGE_FUNCTION(self, test_message=False, request=request)

    def send_test(self, recipient, sender):
        self._send_internal_message(recipient, sender)

    def _send_internal_message(self, recipient, sender):
        subject = self.subject
        from_email = sender
        to_list = recipient.split(',')
        text_content = self.text
        html_content = self.html
        msg = EmailMultiAlternatives(subject,
                                     text_content,
                                     from_email,
                                     to_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def upload(self, re_upload=False):
        files_to_remove = []

        drupal_create_script = ""
        if not re_upload:
            if self.newsletter.drupal_create_script:
                with tempfile.NamedTemporaryFile(delete=False) as f:
                    create_script = render_to_string(
                        self.newsletter.drupal_create_script,
                        dict(issue=self))
                    f.write(create_script.encode('utf8'))
                    drupal_create_script = f.name

                files_to_remove.append(drupal_create_script)

        if self.newsletter.upload_script:
            with tempfile.NamedTemporaryFile(delete=False) as f:
                f.write(self.html_with_tracking.encode('utf8'))
                html_file_path = f.name

            files_to_remove.append(html_file_path)

            name = self.html_file_name
            script_name = self.newsletter.upload_script
            process = subprocess.Popen([script_name,
                                        name,
                                        html_file_path,
                                        drupal_create_script])
            process.wait()

        for file_path in files_to_remove:
            os.remove(file_path)

    @property
    def html_file_name(self):
        filename = "{}_{}.html".format(self.newsletter.title,
                                       self.issue_date.strftime("%B_%d_%Y")
                                      ).lower()

        keep_characters = ('.', '_')
        filename = "".join(c for c in filename
                           if c.isalnum() or c in keep_characters)

        return filename.lower().rstrip()

    @property
    def subject(self):
        subject = render_to_string(self.subject_template,
                                   dict(issue=self))

        return subject

    @property
    def html(self):
        html_body = render_to_string(self.html_email_template,
                                     dict(issue=self, tracking=False, clicks=False))

        return html_body


    @property
    def html_with_tracking(self):
        html_body = render_to_string(self.html_email_template,
                                     dict(issue=self, tracking=True, clicks=False))

        return html_body


    @property
    def text(self):
        txt_body = render_to_string(self.plain_text_email_template,
                                    dict(issue=self, tracking=False, clicks=False))

        return txt_body


    @property
    def text_with_tracking(self):
        txt_body = render_to_string(self.plain_text_email_template,
                                    dict(issue=self, tracking=True, clicks=False))

        return txt_body

    @property
    def name(self):
        return '%s: %s' % (self.newsletter.title,
                           self.issue_date.strftime("%B %Y"))

    def get_stories(self, category):
        stories = NewsItem.objects.filter(issue=self,
                                          feature_type=category
        ).order_by('weight')
        return stories

    def get_top_stories(self, count):
        stories = NewsItem.objects.filter(issue=self
        ).order_by('feature_type__weight', 'weight')[:count]
        return stories

    def __str__(self):
        if self.issue_date:
            return "%s" % self.name
        else:
            return '%s' % self.id


# Definition of news items type that can be included in a newsletter.
# This allows for different types of news items to be treated differently
# depending on the newsletter or position
# within the newsletter
@python_2_unicode_compatible
class FeatureType(models.Model):
    name = models.CharField(max_length=20)
    display_title = models.CharField(max_length=1024)
    max_title_length = models.IntegerField()
    max_description_length = models.IntegerField()
    display_image = models.BooleanField(default=True)
    image_required = models.BooleanField(default=False)
    max_image_width = models.IntegerField(null=True, blank=True)
    max_image_height = models.IntegerField(null=True, blank=True)
    is_headline = models.BooleanField(default=False)
    weight = models.IntegerField(default=0)

    def __str__(self):
        return "%s" % self.name

    @property
    def code_name(self):
        return slugify(self.name)


# Individual news item created as part of a particular issue of a
# selected newsletter
@python_2_unicode_compatible
class NewsItem(models.Model):
    title = RichTextField(max_length=1024, default="", blank=True, null=True)
    url = models.URLField("Link to story", default="", blank=True, null=True)
    description = RichTextField(default="", blank=True, null=True)
    by_line = models.CharField(max_length=1024, default="", blank=True, null=True)
    image = models.ImageField(upload_to=get_upload_folder, null=True,
                              blank=True)
    scaled_image = models.ImageField(upload_to=get_upload_folder, null=True,
                                     blank=True)
    feature_type = models.ForeignKey("FeatureType")
    issue = models.ForeignKey("Issue")
    weight = models.IntegerField(default=0, blank=True)

    class Meta:
        ordering = ('weight', )

    def is_complete(self):
        errors = []

        if not self.title:
            errors.append("Missing title")
        if not self.url:
            errors.append("Missing link to story")
        if not self.description:
            errors.append("Missing short description")

        if self.feature_type.image_required:
            if not self.image:
                errors.append("Missing image")

        return errors

    def image_path(self):
        if self.scaled_image:
            return self.scaled_image.url
        elif self.image:
            return self.image.url
        else:
            return None

    def image_width(self):
        return self.feature_type.max_image_width

    def image_height(self):
        return self.feature_type.max_image_height

    def save(self, *args, **kwargs):
        super(NewsItem, self).save(*args, **kwargs)
        if self.image and not self.scaled_image:
            image_manipulator = ImageManipulator()
            scaled_image_filename, upload = image_manipulator.scale(self.image,
                                                                    smart_text(
                                                                        "{}x{}").format(
                                                                        self.feature_type.max_image_width,
                                                                        self.feature_type.max_image_height))
            if upload:
                self.scaled_image.save(scaled_image_filename,
                                       upload, save=True)

    @property
    def clicks(self):
        link_clicks = settings.MAILER_CLICK_MODEL.objects.filter(click_link__startswith=self.url)
        return len(link_clicks)

    def __str__(self):
        return "%s - %s" % (self.title, self.id)



# Defines a path to a template and defines which types of
# features can be included in this particular template
@python_2_unicode_compatible
class Template(models.Model):
    name = models.CharField(max_length=100)
    filepath = models.CharField(max_length=1024)
    plain_text_filepath = models.CharField(max_length=1024, null=True,
                                           blank=True)
    subject_filepath = models.CharField(max_length=1024, null=True, blank=True)
    supported_feature_types = models.ManyToManyField("FeatureType", null=True,
                                                     blank=True)

    def __str__(self):
        return '%s' % self.name


@python_2_unicode_compatible
class TemplateAttribute(models.Model):
    name = models.CharField(max_length=100)
    value = models.TextField()
    template = models.ForeignKey("Template")

    def __str__(self):
        return "%s - %s" % (self.template.filepath, self.name)


@python_2_unicode_compatible
class TemplateMediaFile(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=get_template_upload_folder,
                              null=True, blank=True)
    template = models.ForeignKey("Template")

    def __str__(self):
        return "%s - %s" % (self.template.filepath, self.name)