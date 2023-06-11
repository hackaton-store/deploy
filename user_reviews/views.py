from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated


from user_reviews.models import Like, Review
from user_reviews.serializers import LikeSerializer, ReviewSerializer
from permissions.permissions import IsOwner


class ReviewViewSet(ModelViewSet):
   
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer



    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]

        else:
            self.permission_classes = [IsOwner]
        return super().get_permissions()
    

class LikeViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer

    def get_queryset(self):

        return Like.objects.filter(user=self.request.user)