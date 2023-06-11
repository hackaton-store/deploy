from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class AbstractCarModel(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey('product.Car', on_delete=models.CASCADE)

    class Meta:

        abstract = True



class RatingChoices(models.IntegerChoices):

    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5



class Rating(AbstractCarModel):
    
    rate = models.PositiveIntegerField(choices=RatingChoices.choices)


    def __str__(self):
        return str(self.rate)
    
    
    class Meta:
        default_related_name = 'rates'
        unique_together = ('user', 'car')
    

class Saved(AbstractCarModel):
    pass

    class Meta:
        default_related_name = 'saved'
        unique_together = ('user', 'car')



class Comment(AbstractCarModel):
    
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f'Comment from {self.user.username}'
    
    class Meta:
        default_related_name = 'comments'