from rest_framework import serializers
from django.contrib.auth import get_user_model


from transactions.models import Balance, TransactionHistory
from product.models import Car


User = get_user_model()


class BalanceSerializer(serializers.ModelSerializer):
   
   
    class Meta:

        model = Balance
        fields = ['user', 'total_balance']
        read_only_fields = ['user']


    def create(self, validated_data):
        request = self.context['request']
        user = validated_data.get('user', request.user)

        
        if hasattr(user, 'balance'):
            raise serializers.ValidationError('You have already created a balance.')

        balance = Balance.objects.create(user=user)
        return balance



class BalanceTopUpSerializer(serializers.Serializer):

    amount = serializers.DecimalField(max_digits=9, decimal_places=2)


    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Amount must be a positive number')
        return value

    
    
class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = '__all__'
        read_only_fields = ['user', 'transaction_time', 'seller']

    def create(self, validated_data):
        user = self.context['request'].user
        product_id = validated_data['product']

        try:
            balance = Balance.objects.get(user=user)
        except Balance.DoesNotExist:
            raise serializers.ValidationError("User balance does not exist")


        try:
            product = Car.objects.get(id=product_id)
            price = product.price
            seller = product.user
            

        except Car.DoesNotExist:
            raise serializers.ValidationError("Product does not exist")

        if balance.total_balance < price:
            raise serializers.ValidationError("Insufficient balance")


        balance.total_balance -= price
        balance.save()
        top_up_balance = Balance.objects.get(user=seller)
        top_up_balance.total_balance +=price
        top_up_balance.save()

        transaction = TransactionHistory.objects.create(
            user=user, product=product_id, price=price, seller = seller
        )
        return transaction

