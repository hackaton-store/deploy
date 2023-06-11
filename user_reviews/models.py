from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()






class Review(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_recieved')
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f'Review from {self.user.username}'
    

    class Meta:
        default_related_name = 'reviews'



class Like(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_given')
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_recieved')

    class Meta:
        default_related_name = 'likes'
        unique_together = ('user', 'to')

