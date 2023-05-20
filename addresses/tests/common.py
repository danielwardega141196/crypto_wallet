import datetime

import mock
from model_bakery import baker

from addresses.models import CurrencyAddress


def create_address_with_specified_datetime(
    creation_datetime: datetime.datetime, **kwargs
) -> CurrencyAddress:
    with mock.patch('django.utils.timezone.now') as mock_now:
        mock_now.return_value = creation_datetime
        return baker.make(_model='addresses.CurrencyAddress', **kwargs)
