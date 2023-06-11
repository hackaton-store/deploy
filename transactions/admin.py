from django.contrib import admin
from transactions.models import TransactionHistory, Balance

admin.site.register([TransactionHistory, Balance])