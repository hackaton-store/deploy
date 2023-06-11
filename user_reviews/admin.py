from django.contrib import admin

from user_reviews.models import Review, Like

admin.site.register([Review, Like])
