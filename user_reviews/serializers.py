from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST


from user_reviews.models import Review, Like


class AbstractListSerializer(serializers.ListSerializer):
    pass


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['review_text', 'to']
        
        read_only_fields = ['user', 'created_at']
    

    def save(self, **kwargs):
        user = self.context.get('request').user
        self.validated_data['user'] = user
        return super().save(**kwargs)


    def update(self, instance, validated_data):
        instance.review_text = validated_data.get('review_text', instance.review_text)
        instance.save()
        return instance


    def partial_update(self, instance, validated_data):
        return self.update(instance, validated_data)
    


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['to'] = instance.to.username
        representation['user'] = instance.user.username
        return representation
 
 
    list_serializer_class = AbstractListSerializer



class LikeSerializer(serializers.ModelSerializer):
  

    class Meta:

        model = Like
        fields = '__all__'
        read_only_fields = ['user']


    def validate(self, attrs):
        user = self.context.get('request').user
        to = attrs.get('to')
        liked = Like.objects.filter(user=user, to=to)

        if liked.exists():
            raise serializers.ValidationError('You already liked this user')
        
        return super().validate(attrs)


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.username
        representation['to'] = instance.to.username
        return representation
    

    def save(self, **kwargs):
        user = self.context.get('request').user
        self.validated_data['user'] = user
        return super().save(**kwargs)
    

    def update(self, instance, validated_data):
        
        raise serializers.ValidationError({'message': 'method not allowed'})


    def partial_update(self, instance, validated_data):
        return self.update(instance, validated_data)
    

    list_serializer_class = AbstractListSerializer