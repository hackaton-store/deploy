from rest_framework import routers

from product.views import CarViewSet

router = routers.DefaultRouter()
router.register("cars", CarViewSet, basename="cars")

urlpatterns = router.urls
