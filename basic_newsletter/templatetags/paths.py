from django import template
from basic_newsletter.models import TemplateMediaFile, TemplateAttribute
import re

register = template.Library()


@register.filter
def media_url(template, media_name):
    template_media_files = TemplateMediaFile.objects.filter(template=template,
                                                            name=media_name)

    if len(template_media_files) > 0:
        return template_media_files[0].image.url


@register.filter
def get_stories(issue, category):
    stories = issue.get_stories(category).all()
    return stories


@register.filter
def tweetify(text):
    p = re.compile(r'\(@(?P<handle>\w*)\)', re.IGNORECASE)
    twitter_handle = p.search(text)
    if twitter_handle:
        tweetified_text = text[:twitter_handle.start()+1] + \
                          "<a href='https://twitter.com/" + \
                          twitter_handle.group('handle') + \
                          "' style='color:#5dd7fc'>" + \
                          twitter_handle.group()[1:-1] + \
                          "</a>" + tweetify(text[twitter_handle.end()-1:])
        return tweetified_text
    else:
        return text


@register.filter
def get_attribute(template, attribute_name):
    template_attributes = TemplateAttribute.objects.filter(template=template,
                                                           name=attribute_name)

    if len(template_attributes) > 0:
        return template_attributes[0].value


@register.simple_tag
def base_styles(tag):
    if tag == 'body':
        return '-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; ' \
               'height: 100% !important; margin: 0; padding: 0; ' \
               'width: 100% !important;'
    elif tag == '#bodyTable' or tag == '#bodyCell':
        return 'height: 100% !important; margin: 0; padding: 0; ' \
               'width: 100% !important;'
    elif tag == 'table':
        return '-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;' \
               ' border-collapse: collapse; mso-table-lspace: 0pt; ' \
               'mso-table-rspace: 0pt;'
    elif tag == 'td':
        return '-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; ' \
               'mso-table-lspace: 0pt; mso-table-rspace: 0pt;'
    elif tag == 'a':
        return 'text-decoration: none; -webkit-text-size-adjust: 100%; ' \
               '-ms-text-size-adjust: 100%;'
    elif tag == 'img':
        return 'border: 0; outline: none; text-decoration: none; ' \
               '-ms-interpolation-mode: bicubic;'
    elif tag == 'p':
        return '-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;'
    elif tag == 'li':
        return '-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;'
    elif tag == 'blockquote':
        return '-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;'
    return ""


