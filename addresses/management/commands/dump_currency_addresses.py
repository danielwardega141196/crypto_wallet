# management/commands/dump_currency_addresses.py

import csv
import datetime

from django.core.management.base import BaseCommand

from addresses.serializers import CurrencyAddressWholeRecordSerializer
from addresses.services import CurrencyAddressService


class Command(BaseCommand):
    help = 'Dump Currency Addresses to CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            'path',
            type=str,
            help='Path to the output csv file',
        )
        parser.add_argument(
            'date',
            type=str,
            help='Creation date of a currency address',
        )

    def handle(self, *args, **kwargs) -> None:
        serializer = CurrencyAddressWholeRecordSerializer
        fieldnames = serializer._declared_fields.keys()
        creation_date = datetime.datetime.strptime(
            kwargs['date'], "%Y-%m-%d"
        ).date()
        currency_addresses = (
            CurrencyAddressService.get_addresses_with_specified_date(
                creation_date=creation_date
            )
        )
        data = serializer(instance=currency_addresses, many=True).data
        with open(kwargs['path'], 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
