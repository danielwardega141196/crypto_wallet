import uuid

from django.db import models

from addresses.constants import (
    ADDRESS_LENGTH,
    PRIVATE_KEY_VERSION_LENGTH,
    SYMBOL_LENGTH,
    Currencies,
)


class CurrencyAddress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address = models.CharField(max_length=ADDRESS_LENGTH)
    symbol = models.CharField(
        max_length=SYMBOL_LENGTH, choices=Currencies.choices
    )
    number = models.PositiveIntegerField()
    private_key_version = models.CharField(
        max_length=PRIVATE_KEY_VERSION_LENGTH
    )
    created_ts = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = [
            '-created_ts',
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['symbol', 'number', 'private_key_version'],
                name="currency_address_number_unique",
            )
        ]
        indexes = [
            models.Index(
                fields=['symbol', 'private_key_version'],
                name='currency_address_number_index',
            )
        ]
