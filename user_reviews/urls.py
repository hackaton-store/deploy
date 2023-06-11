from rest_framework import routers

from user_reviews.views import ReviewViewSet, LikeViewSet

router = routers.DefaultRouter()

router.register('review', ReviewViewSet, basename='review')
router.register('like', LikeViewSet, basename='like')


urlpatterns = router.urls