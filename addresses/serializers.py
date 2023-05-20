from rest_framework import serializers

from addresses.constants import ADDRESS_LENGTH, PRIVATE_KEY_VERSION_LENGTH, Currencies


class CurrencyAddressWholeRecordSerializer(serializers.Serializer):
    id = serializers.CharField()
    address = serializers.CharField(max_length=ADDRESS_LENGTH)
    symbol = serializers.ChoiceField(choices=Currencies.choices)
    number = serializers.IntegerField()
    private_key_version = serializers.CharField(
        max_length=PRIVATE_KEY_VERSION_LENGTH
    )
    created_ts = serializers.DateTimeField()


class CurrencyAddressOnlySymbolSerializer(serializers.Serializer):
    symbol = serializers.ChoiceField(choices=Currencies.choices)
