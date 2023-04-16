from rest_framework import fields, serializers
# from rest_framework_simplejwt.tokens import RefreshToken

from .models import User

class UserSerializer(serializers.ModelSerializer):
    role = serializers.BooleanField(
        read_only = True
    )
    class Meta:
        model = User
        fields = ( 'email', 'id', 'first_name', 'last_name', 'role', 'is_active', 'is_deleted', 'created_at', 'modified_at', 'deleted_at' )


class DonationPostRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)