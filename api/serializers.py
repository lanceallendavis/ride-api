from rest_framework import serializers

from .models import RideUser, Ride, RideEvent


class RideUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideUser
        fields = [
            'id', 
            'username',
            'email', 
            'first_name', 
            'last_name', 
            'role',
            'is_active'
        ]
        read_only_fields = ['id']

class CreateRideUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = RideUser
        fields = [
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'role'
        ]

    def create(self, validated_data):
        user = RideUser(**validated_data)
        user.set_password(validated_data.pop('password'))
        user.save()

        return user


class RideEventSerializer(serializers.ModelSerializer):
    ride = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = RideEvent
        fields = [
            'id',
            'ride',
            'description',
            'created'
        ]
        read_only_fields = ['created']


class RideSerializer(serializers.ModelSerializer):
    rider = RideUserSerializer(read_only=True)
    driver = RideUserSerializer(read_only=True)
    recent_events = RideEventSerializer(many=True, read_only=True)
    distance_km = serializers.SerializerMethodField()

    class Meta:
        model = Ride
        fields = "__all__"

    def get_distance_km(self, obj):
        distance_km = getattr(obj, 'distance_km', None)

        if not distance_km:
            return None

        return round(distance_km, 2)


class CreateRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = [
            'rider',
            'driver',
            'pickup_lat',
            'pickup_long',
            'dropoff_lat',
            'dropoff_long',
            'pickup_time'
        ]
