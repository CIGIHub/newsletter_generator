# newsletter-generator
A Django app to provide ability to generate newsletters.

To use:

Add to INSTALLED_APPS

Add settings for:
MAILER_CAMPAIGN_MODEL = basic_newsletter.mailer_provider_base.CampaignBase
MAILER_ACCOUNT_MODEL = basic_newsletter.mailer_provider_base.AccountBase
MAILER_MESSAGE_MODEL = basic_newsletter.mailer_provider_base.MessageBase
MAILER_LIST_MODEL = basic_newsletter.mailer_provider_base.ListBase
MAILER_UPLOAD_MESSAGE_FUNCTION = basic_newsletter.mailer_provider_base.dummy_upload_message
MAILER_SEND_MESSAGE_FUNCTION = basic_newsletter.mailer_provider_base.dummy_send_message

customize these settings as desired:
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_JQUERY_URL = "http://code.jquery.com/jquery-1.9.1.js"

CKEDITOR_CONFIGS = {
           'default': {
               'toolbar': 'Basic',
               'height': 300,
               'width': 560,
               'autoParagraph': False,
           },
           'headline_title': {
               'toolbar': 'Basic',
               'height': 40,
               'width': 560,
               'autoParagraph': False,
           },
           'headline_description': {
               'toolbar': 'Basic',
               'height': 300,
               'width': 560,
               'autoParagraph': False,
           },
           'item_title': {
               'toolbar': 'Basic',
               'height': 40,
               'width': 260,
               'autoParagraph': False,
           },
           'item_description': {
               'toolbar': 'Basic',
               'height': 150,
               'width': 260,
               'autoParagraph': False,
           },
       }


Run migrations