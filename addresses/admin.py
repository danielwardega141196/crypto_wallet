from django.contrib import admin

from addresses.models import CurrencyAddress


@admin.register(CurrencyAddress)
class CurrencyAddressAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'address',
        'symbol',
        'number',
        'private_key_version',
        'created_ts',
    )
    search_fields = (
        '=id',
        '=address',
        '=symbol',
        '=number',
        '=private_key_version',
    )
    fields = (
        'id',
        'address',
        'symbol',
        'number',
        'private_key_version',
        'created_ts',
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
