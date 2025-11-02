from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response

from .models import RideUser
from .serializers import RideUserSerializer, CreateRideUserSerializer
from .permissions import IsRideUserAdmin

class RideUserViewset(viewsets.ReadOnlyModelViewSet):
    """
    - 'CRUD' for Users(RideUser)
    """

    queryset = RideUser.objects.all()
    serializer_class = RideUserSerializer
    permission_classes = [IsRideUserAdmin, IsAdminUser]

    # Create/register new user
    @action(
        detail=False,
        methods=['post'],
        serializer_class=CreateRideUserSerializer,
    )
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "data": RideUserSerializer(user).data,
                "message": f"{user.username} is registered successfully.",
                "status": "success"}
            , 
            status=status.HTTP_200_OK
        )

    # Update user role (separated from updating user's personal information)
    # as it is a different 'concern'.
    @action(
        detail=True,
        methods=['post'],
    )
    def update_role(self, request, pk=None):
        role = request.data.get('role')
        valid_roles = [choice[0] for choice in RideUser.RoleChoices.choices]
        if role not in valid_roles:
            
            return Response({
                "error": "Invalid role requested. ",
                "status": "failed"
            },status=status.HTTP_400_BAD_REQUEST)
        
        user = self.get_object() 
        current_role = user.get_role_display()       
        user.role = role
        user.save()
        updated_role = user.get_role_display()

        return Response({
            "message": f"{user.username}'s role updated from {current_role} to {updated_role}. ",
            "status": "success"
        }, status=status.HTTP_200_OK)
    
    # Soft-delete user
    @action(
        detail=True,
        methods=['post']
    )
    def set_inactive(self, request, pk=None):
        user = self.get_object()
        if not user.is_active:
            return Response(
                {
                    "message": f"{user.username} is already set to inactive. ",
                    "status": "failed"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.is_active = False
        user.save()

        return Response(
            {
                "message": f"{user.username} is set to inactive. ",
                "status": "success"
        }, status=status.HTTP_200_OK)
    
    # Update user information(separated from changing roles/soft-delete)
    @action(
        detail=True,
        methods=['patch']
    )
    def update_user(self, request, pk=None):
        valid_fields = [
            'first_name', 
            'last_name', 
            'email', 
            'phone_number'
        ]

        # Check unwanted/invalid fields in the request
        invalid_fields = [field for field in request.data if field not in valid_fields]
        if invalid_fields:
            return Response({
                "message": f"Invalid fields: {', '.join(invalid_fields)}",
                "status": "failed"
            }, status=status.HTTP_400_BAD_REQUEST)
        user = self.get_object()

        for field in valid_fields:
            if field in request.data:
                setattr(user, field, request.data[field])
        user.save()

        return Response({
            "data": RideUserSerializer(user).data,
            "message": f"{user.username}'s user information is updated.",
            "status": "success"
        }, status=status.HTTP_200_OK)