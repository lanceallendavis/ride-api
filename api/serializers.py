from rest_framework import serializers

from .models import RideUser


class RideUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideUser
        fields = [
            'id', 
            'username', 
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
