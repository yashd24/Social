from rest_framework import serializers
from .models import CustomUser,Friend_Request

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','name', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class FriendRequestSerializer(serializers.ModelSerializer):
    sent_by = CustomUserSerializer(read_only=True)
    sent_to = CustomUserSerializer(read_only=True)

    class Meta:
        model = Friend_Request
        fields = '__all__'