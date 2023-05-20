import datetime
from uuid import uuid4

from django.test import TestCase
from django.urls import reverse
from mock import patch
from rest_framework import serializers
from rest_framework.test import APIClient

from addresses.services import CurrencyAddressService
from addresses.tests.common import create_address_with_specified_datetime


class TestAddressViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list(self):
        first_id = uuid4()
        first_created_ts = datetime.datetime(2020, 2, 15, 1)
        create_address_with_specified_datetime(
            creation_datetime=first_created_ts,
            id=first_id,
            address='first_address',
            symbol='ETH',
            number=1,
            private_key_version='v54',
        )
        second_id = uuid4()
        second_created_ts = datetime.datetime(2020, 2, 15, 2)
        create_address_with_specified_datetime(
            creation_datetime=second_created_ts,
            id=second_id,
            address='second_address',
            symbol='DOGE',
            number=1,
            private_key_version='v54',
        )
        third_id = uuid4()
        third_created_ts = datetime.datetime(2020, 2, 15, 3)
        create_address_with_specified_datetime(
            creation_datetime=third_created_ts,
            id=third_id,
            address='third_address',
            symbol='BTC',
            number=1,
            private_key_version='v54',
        )
        list_url = reverse('addresses-list')
        response = self.client.get(list_url).json()

        expected_result = [
            {
                "id": str(third_id),
                "address": "third_address",
                "symbol": "BTC",
                "number": 1,
                'private_key_version': 'v54',
                'created_ts': serializers.DateTimeField().to_representation(
                    third_created_ts
                ),
            },
            {
                "id": str(second_id),
                "address": "second_address",
                "symbol": "DOGE",
                "number": 1,
                'private_key_version': 'v54',
                'created_ts': serializers.DateTimeField().to_representation(
                    second_created_ts
                ),
            },
            {
                "id": str(first_id),
                "address": "first_address",
                "symbol": "ETH",
                "number": 1,
                'private_key_version': 'v54',
                'created_ts': serializers.DateTimeField().to_representation(
                    first_created_ts
                ),
            },
        ]
        self.assertListEqual(response, expected_result)

    def test_retrieve(self):
        address_id = uuid4()
        created_ts = datetime.datetime(2021, 9, 11)
        create_address_with_specified_datetime(
            creation_datetime=created_ts,
            id=address_id,
            address='dash_address',
            symbol='DASH',
            number=1,
            private_key_version='v98',
        )
        detail_url = reverse(
            'addresses-detail', kwargs={"pk": str(address_id)}
        )

        response = self.client.get(detail_url).json()

        self.assertDictEqual(
            response,
            {
                "id": str(address_id),
                "address": "dash_address",
                "symbol": "DASH",
                "number": 1,
                'private_key_version': 'v98',
                'created_ts': serializers.DateTimeField().to_representation(
                    created_ts
                ),
            },
        )

    @patch.object(CurrencyAddressService, "create_currency_address")
    def test_create(self, create_address_record_mock):
        address_id = uuid4()
        created_ts = datetime.datetime.utcnow()
        address_data = {
            'id': address_id,
            'address': 'test_address',
            'symbol': 'DASH',
            'number': 0,
            'private_key_version': 'private_key_version',
            'created_ts': created_ts,
        }
        create_address_record_mock.return_value = address_data

        response = self.client.post(
            '/addresses/', data={"symbol": 'DOGE'}
        ).json()

        create_address_record_mock.assert_called_once()
        self.assertDictEqual(
            response,
            {
                'id': str(address_id),
                'address': 'test_address',
                'symbol': 'DASH',
                'number': 0,
                'private_key_version': 'private_key_version',
                'created_ts': serializers.DateTimeField().to_representation(
                    created_ts
                ),
            },
        )
