from rest_framework import routers

from car_reviews.views import CommentViewSet, RatingViewSet, SavedViewSet

router = routers.DefaultRouter()


router.register('comment', CommentViewSet, basename='comment')
router.register('rating', RatingViewSet, basename='rating')
router.register('saved', SavedViewSet, basename='saved')

urlpatterns = router.urls