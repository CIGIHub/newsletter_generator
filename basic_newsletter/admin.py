from django import forms
from django.forms import models
from django.contrib import admin
from basic_newsletter.models import Newsletter, Issue, FeatureType, NewsItem, \
    Template, TemplateMediaFile, TemplateAttribute, GoogleAnalyticsCampaign


class NewsItemForm(models.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'title'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'description'}), required=False)

    class Meta:
        model = NewsItem
        exclude = []


class TemplateMediaFileInline(admin.TabularInline):
    model = TemplateMediaFile


class TemplateAttributeInline(admin.TabularInline):
    model = TemplateAttribute


class GoogleAnalyticsInline(admin.TabularInline):
    model = GoogleAnalyticsCampaign


class NewsItemInline(admin.StackedInline):
    model = NewsItem
    form = NewsItemForm


class NewsItemAdmin(admin.ModelAdmin):
    model = NewsItem
    form = NewsItemForm


class TemplateAdmin(admin.ModelAdmin):
    model = Template
    inlines = (TemplateMediaFileInline, TemplateAttributeInline, )


class NewsletterAdmin(admin.ModelAdmin):
    model = Newsletter
    inlines = (GoogleAnalyticsInline, )


class IssueAdmin(admin.ModelAdmin):
    model = Issue
    inlines = (NewsItemInline, )


admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(FeatureType)
admin.site.register(NewsItem, NewsItemAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(TemplateMediaFile)
admin.site.register(TemplateAttribute)
admin.site.register(GoogleAnalyticsCampaign)
