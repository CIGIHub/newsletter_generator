from django.contrib import admin
from basic_newsletter.models import Newsletter, Issue, FeatureType, NewsItem, \
    Template, TemplateMediaFile, TemplateAttribute


class TemplateMediaFileInline(admin.TabularInline):
    model = TemplateMediaFile


class TemplateAttributeInline(admin.TabularInline):
    model = TemplateAttribute


class TemplateAdmin(admin.ModelAdmin):
    model = Template
    inlines = (TemplateMediaFileInline, TemplateAttributeInline, )


admin.site.register(Newsletter)
admin.site.register(Issue)
admin.site.register(FeatureType)
admin.site.register(NewsItem)
admin.site.register(Template, TemplateAdmin)
admin.site.register(TemplateMediaFile)
admin.site.register(TemplateAttribute)
