from django.contrib import admin

from  car_reviews.models import Comment, Rating, Saved

admin.site.register([Comment, Rating, Saved])
