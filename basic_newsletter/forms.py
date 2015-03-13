from django.forms import ModelForm, DateField, Form, ChoiceField, \
    CharField, EmailField, MultipleChoiceField
from django.forms.widgets import Textarea, TextInput
from basic_newsletter.models import Issue, NewsItem, Newsletter, FeatureType
from basic_newsletter.widgets import MonthYearWidget
from django.utils.functional import lazy
from ckeditor.widgets import CKEditorWidget


def get_newsletter_types():
    newsletters = Newsletter.objects.all()
    types = []
    for newsletter in newsletters:
        types.append((newsletter.id, newsletter.title))

    return tuple(types)


def get_story_categories():
    categories = FeatureType.objects.all()
    types = []
    for category in categories:
        types.append((category.id, category.display_title))

    return tuple(types)


class CreateIssueForm(Form):
    newsletter_type = ChoiceField(choices=lazy(get_newsletter_types, tuple)())
    issue_date = DateField(widget=MonthYearWidget)
    sections = MultipleChoiceField(choices=lazy(get_story_categories, tuple)())


class EmailTestForm(Form):
    recipient = CharField(max_length=2048, widget=Textarea)
    sender = EmailField()


class IssueForm(ModelForm):
    published_date = DateField(widget=MonthYearWidget)

    class Meta:
        model = Issue
        exclude = ['template']


class NewsItemForm(ModelForm):
    title = CharField(widget=CKEditorWidget(config_name='item_title'))
    description = CharField(widget=CKEditorWidget(config_name='item_description'))

    class Meta:
        model = NewsItem
        fields = ('title', 'url', 'description', 'weight')


class HeadlineNewsItemForm(ModelForm):
    title = CharField(widget=CKEditorWidget(config_name='headline_title'))
    description = CharField(widget=CKEditorWidget(config_name='headline_description'))

    class Meta:
        model = NewsItem
        fields = ('title', 'url', 'image', 'description', 'weight')
