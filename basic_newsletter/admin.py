from django.contrib import admin
from basic_newsletter.models import Newsletter, Issue, FeatureType, NewsItem, \
    Template, TemplateMediaFile, TemplateAttribute, GoogleAnalyticsCampaign


class TemplateMediaFileInline(admin.TabularInline):
    model = TemplateMediaFile


class TemplateAttributeInline(admin.TabularInline):
    model = TemplateAttribute


class GoogleAnalyticsInline(admin.TabularInline):
    model = GoogleAnalyticsCampaign


class TemplateAdmin(admin.ModelAdmin):
    model = Template
    inlines = (TemplateMediaFileInline, TemplateAttributeInline, )


class NewsletterAdmin(admin.ModelAdmin):
    model = Newsletter
    inlines = (GoogleAnalyticsInline, )


admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Issue)
admin.site.register(FeatureType)
admin.site.register(NewsItem)
admin.site.register(Template, TemplateAdmin)
admin.site.register(TemplateMediaFile)
admin.site.register(TemplateAttribute)
admin.site.register(GoogleAnalyticsCampaign)
