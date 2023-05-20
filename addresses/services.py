import datetime
from typing import Optional

from django.db.models import Max
from django.db.models.query import QuerySet
from hdwallet import HDWallet

from addresses.constants import Currencies
from addresses.models import CurrencyAddress


class CurrencyAddressService:
    @staticmethod
    def generate_address(
        symbol: Currencies.names, number: int, private_key: str
    ) -> str:
        """
        Function takes a wallet using 'private_key' as a seed
        and 'number' as a number of a cryptocurrency address generated
        for a given currency's 'symbol' and a given 'private_key'

        :param symbol: a symbol from 'Currencies' enum representing a cryptocurrency
        :type symbol: string - str
        :param number: number of cryptocurrency type identified
        with a given private key (private_key_version)
        :type number: integer - int
        :param private_key: private key that will be used
        as a seed to take a cryptocurrency wallet
        :type private_key: string - str
        :return: unique address assigned to a cryptocurrency with a given symbol
        :rtype: string - str
        """
        hdwallet: HDWallet = HDWallet(symbol=symbol)
        hdwallet.from_seed(private_key)
        hdwallet.from_index(number)
        return hdwallet.address()

    @staticmethod
    def get_last_number(
        symbol: Currencies.names, private_key_version: str
    ) -> Optional[int]:
        """
        Function seeks for and returns last number assigned
        to a given 'symbol' and a given 'private_key_version'

        :param symbol: a symbol from 'Currencies' enum representing a cryptocurrency
        :type symbol: string - str
        :param private_key_version: a version under which the private key is located
        :type private_key_version: string - str
        :return: last number assigned to a given 'symbol' and a given 'private_key_version'
        :rtype: integer - int or None
        """
        return CurrencyAddress.objects.filter(
            symbol=symbol, private_key_version=private_key_version
        ).aggregate(Max('number'))['number__max']

    @classmethod
    def create_currency_address(
        cls,
        symbol: Currencies.names,
        private_key_version: str,
        private_key: str,
    ) -> CurrencyAddress:
        """
        Function creates, saves and returns a new address
        for a cryptocurrency with a given 'symbol'
        with the use of 'private_key_version' and 'private_key'

        :param symbol: a symbol from 'Currencies' enum representing a cryptocurrency
        :type symbol: string - str
        :param private_key_version: a version under which the private key is located
        :type private_key_version: string - str
        :param private_key: private key that will be used
        as a seed to take a cryptocurrency wallet
        :type private_key: string - str
        :return: a new address for a cryptocurrency with a given 'symbol'
        generated with use of 'private_key_version' and 'private_key'
        :rtype: CurrencyAddress(django.db.models.base.Model)
        """
        last_number = cls.get_last_number(
            symbol=symbol,
            private_key_version=private_key_version,
        )
        number = 0 if last_number is None else last_number + 1
        address = cls.generate_address(
            symbol=symbol, number=number, private_key=private_key
        )
        return CurrencyAddress.objects.create(
            address=address,
            symbol=symbol,
            private_key_version=private_key_version,
            number=number,
        )

    @staticmethod
    def get_addresses_with_specified_date(
        creation_date: datetime.date,
    ) -> QuerySet:
        """
        Function seeks for and returns addresses
        created on the 'creation_date'

        :param creation_date: creation date of the addresses we are looking for
        :type creation_date: datetime.date
        :return: QuerySet with addresses created on the 'creation_date'
        :rtype: QuerySet(django.db.models.query.QuerySet)
        """
        return CurrencyAddress.objects.filter(
            created_ts__date=creation_date
        ).all()
