from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend




from permissions.permissions import IsModeratorOrIsAdminUser, IsOwnerOrIsModeratorOrIsAdminUser
from product.models import Car
from product.serializers import CarSerializer, OneCarSerializer
from .utils import CarFilter



def check_user(request: Request):
    if not request.user.is_anonymous:
        if (request.user.is_staff or request.user.is_moderator):
            return True
    return False
        


class CarViewSet(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = CarFilter

    filterset_fields = ['brand', 'color']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'release']
    


    def list(self, request: Request, *args, **kwargs):
        queryset = self.filter_queryset(Car.objects.filter(status='published').order_by('-id'))
        check = check_user(request)
        if check:
            queryset = Car.objects.all().order_by('-id')




        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

    

        

    def retrieve(self, request, *args, **kwargs):

        self.serializer_class = OneCarSerializer
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        recommendations = Car.objects.exclude(id=instance.id).all()
        recommendations_serializer = CarSerializer(recommendations, many=True)
        serialized_data = serializer.data

        instance_brand = serializer.data['brand']
        list_of_recommendations = recommendations_serializer.data

        filtered_list_of_recommendations = [car for car in list_of_recommendations if car['brand'] == instance_brand]

                
        sorted_list_of_recommendations = sorted(filtered_list_of_recommendations, key=lambda x: x['rating'], reverse=True)

        serialized_data['recommendations'] = sorted_list_of_recommendations


        is_staff = check_user(request)
        if is_staff is not True:
            if self.get_object().status == 'processing':
                return Response({'message':'You have no permission to see this page'}, status=400)
            elif self.get_object().status == 'published':
                return Response(serialized_data)

        else:
                return Response(serialized_data)



    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [AllowAny]
        elif self.request.method in "POST":
            if self.request.data.get('status'):
                self.permission_classes = [IsModeratorOrIsAdminUser]
            self.permission_classes = [IsAuthenticated]
        elif self.request.user.is_anonymous:
            self.permission_classes = [IsAuthenticated]
        else:
            if self.request.data.get('status'):
                self.permission_classes = [IsModeratorOrIsAdminUser]
            else:
                self.permission_classes = [IsOwnerOrIsModeratorOrIsAdminUser]

        return super().get_permissions()







