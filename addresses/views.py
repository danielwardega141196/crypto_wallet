from rest_framework import status
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from addresses.constants import PRIVATE_KEY, PRIVATE_KEY_VERSION
from addresses.models import CurrencyAddress
from addresses.serializers import (
    CurrencyAddressOnlySymbolSerializer,
    CurrencyAddressWholeRecordSerializer,
)
from addresses.services import CurrencyAddressService


class AddressViewSet(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
):
    queryset = CurrencyAddress.objects.all()
    serializer_class = CurrencyAddressWholeRecordSerializer

    def create(self, request: Request, *args, **kwargs) -> Response:
        request_serializer = CurrencyAddressOnlySymbolSerializer(
            data=request.data
        )
        request_serializer.is_valid(raise_exception=True)

        symbol = request_serializer.validated_data['symbol']
        address = CurrencyAddressService.create_currency_address(
            symbol=symbol,
            private_key_version=PRIVATE_KEY_VERSION,
            private_key=PRIVATE_KEY,
        )

        response_serializer = self.get_serializer_class()
        return Response(
            response_serializer(address).data, status=status.HTTP_201_CREATED
        )
