import datetime
from functools import partial
from unittest.mock import MagicMock

from django.test import TestCase
from mock import patch
from model_bakery import baker
from parameterized import parameterized

from addresses.constants import Currencies
from addresses.models import CurrencyAddress
from addresses.services import CurrencyAddressService
from addresses.tests.common import create_address_with_specified_datetime


class TestCurrencyAddressService(TestCase):
    @parameterized.expand(Currencies.names)
    @patch('addresses.services.HDWallet')
    def test_generate_address(self, symbol, hd_wallet_mock):
        hd_wallet_mock_return_value = MagicMock()
        address_mock = MagicMock(return_value="random_address")
        hd_wallet_mock_return_value.address = address_mock
        hd_wallet_mock.return_value = hd_wallet_mock_return_value

        address = CurrencyAddressService.generate_address(
            symbol=symbol, number=987, private_key='xyz'
        )

        self.assertEqual(address, "random_address")
        hd_wallet_mock.assert_called_once_with(symbol=symbol)
        hd_wallet_mock_return_value.from_seed.assert_called_once_with('xyz')
        hd_wallet_mock_return_value.from_index.assert_called_once_with(987)
        address_mock.assert_called_once()

    @parameterized.expand(Currencies.names)
    def test_same_address_for_same_data(self, symbol):
        self.assertEqual(
            CurrencyAddressService.generate_address(
                symbol=symbol, number=0, private_key='abcd'
            ),
            CurrencyAddressService.generate_address(
                symbol=symbol, number=0, private_key='abcd'
            ),
        )

    def test_get_last_number_without_records(self):
        self.assertIsNone(CurrencyAddressService.get_last_number('BTC', 'v1'))

    def test_get_last_number_with_records(self):
        address_btc_model = partial(
            baker.make,
            _model='addresses.CurrencyAddress',
            symbol='BTC',
            private_key_version='v5',
        )
        address_btc_model(number=4)
        address_btc_model(number=6)
        address_btc_model(number=9)

        last_number = CurrencyAddressService.get_last_number('BTC', 'v5')

        self.assertEqual(last_number, 9)

    @patch.object(
        CurrencyAddressService,
        "generate_address",
        return_value='test_first_address',
    )
    @patch.object(CurrencyAddressService, "get_last_number", return_value=None)
    def test_create_address_record_first_address(
        self, get_last_number_mock, generate_address_mock
    ):
        CurrencyAddressService.create_currency_address(
            symbol='ETH', private_key_version='v3', private_key='test_first'
        )

        currency_address = CurrencyAddress.objects.get()
        get_last_number_mock.assert_called_once_with(
            symbol='ETH',
            private_key_version='v3',
        )
        generate_address_mock.assert_called_once_with(
            symbol='ETH', number=0, private_key='test_first'
        )
        self.assertEqual(currency_address.address, 'test_first_address')
        self.assertEqual(currency_address.symbol, 'ETH')
        self.assertEqual(currency_address.private_key_version, 'v3')
        self.assertEqual(currency_address.number, 0)

    @patch.object(
        CurrencyAddressService,
        "generate_address",
        return_value='test_next_address',
    )
    @patch.object(CurrencyAddressService, "get_last_number", return_value=7)
    def test_create_address_record_next_address(
        self, get_last_number_mock, generate_address_mock
    ):
        CurrencyAddressService.create_currency_address(
            symbol='DOGE', private_key_version='v2', private_key='test_next'
        )

        currency_address = CurrencyAddress.objects.get()
        get_last_number_mock.assert_called_once_with(
            symbol='DOGE',
            private_key_version='v2',
        )
        generate_address_mock.assert_called_once_with(
            symbol='DOGE', number=8, private_key='test_next'
        )
        self.assertEqual(currency_address.address, 'test_next_address')
        self.assertEqual(currency_address.symbol, 'DOGE')
        self.assertEqual(currency_address.private_key_version, 'v2')
        self.assertEqual(currency_address.number, 8)

    def test_get_currency_addresses(self):
        time_zone_info = datetime.timezone.utc
        first_model = create_address_with_specified_datetime(
            creation_datetime=datetime.datetime(
                2021, 3, 4, tzinfo=time_zone_info
            ),
        )
        second_model = create_address_with_specified_datetime(
            creation_datetime=datetime.datetime(
                2022, 9, 21, 1, tzinfo=time_zone_info
            ),
        )
        third_model = create_address_with_specified_datetime(
            creation_datetime=datetime.datetime(
                2022, 9, 21, 2, tzinfo=time_zone_info
            ),
        )

        addresses = CurrencyAddressService.get_addresses_with_specified_date(
            creation_date=datetime.date(2022, 9, 21)
        )

        self.assertListEqual(list(addresses), [third_model, second_model])
