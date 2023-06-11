from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


from transactions.serializers import BalanceSerializer, BalanceTopUpSerializer, TransactionHistorySerializer
from transactions.models import Balance, TransactionHistory



class BalanceView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="post balance",
        responses={201: BalanceSerializer()},
    )
    def post(self, request):
        serializer = BalanceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
        
    @swagger_auto_schema(
        operation_description="get balance",
        responses={200: BalanceSerializer()},
    )
    def get(self, request):
        user = request.user
        try:
            balance = Balance.objects.get(user=user)
            serializer = BalanceSerializer(balance)
            return Response(serializer.data)
        except Balance.DoesNotExist:
            return Response(status=404)


class BalanceTopUpView(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Top up balance",
        responses={200: BalanceTopUpSerializer()},
    )
    def post(self, request):
        serializer = BalanceTopUpSerializer(data=request.data, context={'request': request})
       
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
           
            try:
                balance = Balance.objects.get(user=request.user)
            
            except Balance.DoesNotExist:
                balance = Balance.objects.create(user=request.user, total_balance=0)
            
            balance.total_balance += amount
            balance.save()
          
            return Response({'message': 'Balance topped up successfully'}, status=200)
       
        return Response(serializer.errors, status=400)
    

class TransactionHistoryCreateView(CreateAPIView):
    serializer_class = TransactionHistorySerializer
    permission_classes = [IsAuthenticated]


class TransactionHistoryListView(ListAPIView):
    serializer_class = TransactionHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.is_moderator:

            return TransactionHistory.objects.all()

        return TransactionHistory.objects.filter(user=user)
    

class TransactionHistoryDetailView(RetrieveAPIView):
    serializer_class = TransactionHistorySerializer
    queryset = TransactionHistory.objects.all()
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        if not user.is_staff and not user.is_moderator:

            queryset = queryset.filter(user=user)

        return queryset