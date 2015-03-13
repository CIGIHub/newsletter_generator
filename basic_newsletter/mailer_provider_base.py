# This file provides the interface for functions and classes that need to be
# implemented for the related MAILER items.

from django.db import models


def dummy_upload_message(issue, request=None):
    pass


def dummy_send_message(issue, test_message=True, request=None):
    pass


class AccountBase(models.Model):

    class Meta:
        abstract = True


class ListBase(models.Model):

    class Meta:
        abstract = True


class CampaignBase(models.Model):

    class Meta:
        abstract = True


class MessageBase(models.Model):

    class Meta:
        abstract = True
