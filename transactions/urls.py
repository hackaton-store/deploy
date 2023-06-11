from django.urls import path
from .views import BalanceView, BalanceTopUpView, TransactionHistoryCreateView, TransactionHistoryListView, TransactionHistoryDetailView


urlpatterns = [
    path('balance/', BalanceView.as_view(), name='balance-view'),
    path('balance-top-up/', BalanceTopUpView.as_view(), name='balance-top-up'),
    path('transaction-history-create/', TransactionHistoryCreateView.as_view(),  name='transaction-history-create'),
    path('transaction-history/', TransactionHistoryListView.as_view(), name='transaction-history-list'),
    path('transaction-history/<int:pk>/', TransactionHistoryDetailView.as_view(), name='transaction-history-detail')
]