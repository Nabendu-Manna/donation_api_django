from rest_framework import fields, serializers

from accounts.models import User
from accounts.serializers import UserSerializer
from .models import DonationPost


class DonationPostSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = DonationPost
        fields = ('id', 'donation_for', 'amount', 'country', 'state', 'latitude', 'longitude', 'end_date', 'created_at', 'user', 'user_details')


class DonationPostRequestSerializer(serializers.Serializer):
    donation_for = serializers.CharField(required=True)
    amount = serializers.FloatField(required=True)
    country = serializers.CharField(required=True)
    state = serializers.CharField(required=True)
    end_date = serializers.DateField(required=True)
    # user_id = serializers.IntegerField(required=True)
