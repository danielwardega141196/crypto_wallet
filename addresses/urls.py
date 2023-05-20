from rest_framework.routers import SimpleRouter

from addresses.views import AddressViewSet

router = SimpleRouter()
router.register('addresses', AddressViewSet, basename='addresses')

urlpatterns = router.urls
