from datetime import timedelta

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch
from django.utils import timezone

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter

from .models import RideUser, Ride, RideEvent
from .serializers import (
    RideUserSerializer, 
    CreateRideUserSerializer,
    RideSerializer,
    CreateRideSerializer,
    RideEventSerializer
)
from .permissions import IsRideUserAdmin
from .pagination import RidesPagination
from .querysets import calculate_distance


class RideUserViewset(viewsets.ReadOnlyModelViewSet):
    """
    - 'CRUD' for Users(RideUser)
    - Change role, set inactive, and update profile are separated
    since their purposes/concerns differ from one another.
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

        return Response({
            "data": RideUserSerializer(user).data,
            "message": f"{user.username} is registered successfully.",
            "status": "success"
        }, status=status.HTTP_200_OK)

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
            }, status=status.HTTP_400_BAD_REQUEST)
        
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

            return Response({
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
    

class RideViewset(viewsets.ReadOnlyModelViewSet):
    """
    - For Rides (list, create/book, delete ONLY)
    - Edit should not be allowed, in irl: When there's a 
    change of mind, should book a new ride instead. Hence,
    status of ride should be sent as 'cancelled.'
    """
    serializer_class = RideSerializer
    permission_classes = [IsRideUserAdmin, IsAdminUser]
    pagination_class = RidesPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'rider__email']
    ordering_fields = ['pickup_time', 'distance_km']  

    def get_queryset(self):
        cutoff = timezone.now() - timedelta(hours=24)
        recent_events = Prefetch(
            'events',
            queryset=RideEvent.objects.filter(created__gte=cutoff),
            to_attr='recent_events',
        )
        queryset = Ride.objects.select_related('driver', 'rider').prefetch_related(recent_events)

        if self.action == 'list':            
            lat = self.request.query_params.get('lat')
            long = self.request.query_params.get('long')
            
            # Check if calculating distance, need b
            if (lat and not long) or (not lat and long):
                
                return queryset
            
            queryset = calculate_distance(queryset, lat, long)

        return queryset.order_by('-pickup_time')


    # Book or 'create' a ride.
    @action(
        detail=False, 
        methods=['post'],
        serializer_class=CreateRideSerializer
    )
    def book(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ride = serializer.save()

        RideEvent.objects.create(
            ride=ride,
            description=RideEvent.get_description_by_status(Ride.StatusChoices.PICKUP)
        )


        return Response({
            "data": RideSerializer(ride).data,
            "message": f"{ride.rider.username} will be picked up soon.",
            "status": "success"
        }, status=status.HTTP_200_OK)
    
    # Delete ride(NOT SOFT-DELETE)
    @action(
        detail=True,
        methods=['delete']
    )
    def delete_forever(self, request, pk=None):
        ride = self.get_object()
        ride.delete()

        return Response({
            "message": f"Ride {pk} is deleted forever. ",
            "status": "success"
        }, status=status.HTTP_200_OK)
    
    # Update ride status and add as an event
    @action(
        detail=True,
        methods=['post']
    )
    def update_status(self, request, pk=None):
        ride = self.get_object()
        ride_status = request.data.get("status")

        if not ride_status:

            return Response({
                "message": "Status code is required. ", 
                "status": "failed"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if ride_status not in Ride.StatusChoices.values:

            return Response({
                "message": "Status code is required. ", 
                "status": "failed"
            }, status=status.HTTP_404_NOT_FOUND)
        
        ride.status = ride_status
        ride.save()

        try:
            description = RideEvent.get_description_by_status(ride_status)
        except ValueError as e:
            return Response({
                "message": str(e), 
                "status": "failed"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        ride_event = RideEvent.objects.create(ride=ride, description=description)

        return Response({
            "data": RideEventSerializer(ride_event).data,
            "message": f"Ride status changed to '{ride.get_status_display()}'. ",
            "status": "success"
        }, status=status.HTTP_200_OK)


class RideEventViewset(viewsets.ViewSet):
    """
    - Create and Delete only for Ride Events.
    - List of events should be given in Ride Viewset in 'retrieving' a ride.
    - A change in status is an event, but an event is not always a change in status.
    Hence, status change should not be in this endpoint/viewset.
    - Editing should not be allowed because ride events are basically 'historical
    data' and therefore should not be tampered with.
    - Delete is allowed for cleanup/duplicates/accidentals as form for compliance
    """
    permission_classes = [IsRideUserAdmin, IsAdminUser]

    def create(self, request):
        ride_id = request.data.get("ride_id")
        description = request.data.get("description")

        if not ride_id or not description:

            return Response({
                "message": "Both 'ride_id' and 'description' are required. ",
                "status": "failed"
            }, status=status.HTTP_400_BAD_REQUEST)

        ride = get_object_or_404(Ride, id=ride_id)

        ride_event = RideEvent.objects.create(
            ride=ride,
            description=description
        )

        return Response({
            "data": RideEventSerializer(ride_event).data,
            "message": f"Event '{ride_event.description}' is added to ride {ride.id}. ",
            "status": "success"
        }, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        ride_event = get_object_or_404(RideEvent, id=pk)
        ride_event.delete()

        return Response(
            {"message": f"Ride event {pk} deleted successfully.", "status": "success"},
            status=status.HTTP_204_NO_CONTENT
        )