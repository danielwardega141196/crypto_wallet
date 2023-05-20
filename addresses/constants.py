import requests
from django.db import models
from django.utils.translation import gettext_lazy as _


class Currencies(models.TextChoices):
    BTC = 'BTC', _('Bitcoin')
    ETH = 'ETH', _('Ethereum')
    DOGE = 'DOGE', _('Dogecoin')
    LTC = 'LTC', _('Litecoin')
    OMNI = 'OMNI', _('Omni')
    DASH = 'DASH', _('Dash')
    QTUM = 'QTUM', _('Qtum')


PRIVATE_KEY_VERSION = 'v1'


def download_private_key(private_key_version: str) -> str:
    """
    Function downloads and returns
    a private key associated with the 'private_key_version'

    :param private_key_version: a version under which the private key is located
    :type private_key_version: string - str
    :return: private key associated with the 'private_key_version'
    :rtype: string - str
    """

    # For now here is just simply download from S3 but in the future it can be replaced
    # with secret manager which will store the appropriate version of private key and
    # access to it can be limited any time
    url = f'https://crypto-private-keys.s3.amazonaws.com/{private_key_version}.json'
    return requests.get(url).json()['private_key']


PRIVATE_KEY = download_private_key(private_key_version=PRIVATE_KEY_VERSION)

ADDRESS_LENGTH = 256
SYMBOL_LENGTH = 8
PRIVATE_KEY_VERSION_LENGTH = 8
