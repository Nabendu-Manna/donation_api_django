from rest_framework import fields, serializers

from accounts.models import User
from accounts.serializers import UserSerializer
from .models import DonationLog, DonationPost


class DonationPostSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(
        read_only=True,
    )
    received_amount = serializers.IntegerField(read_only=True)

    class Meta:
        model = DonationPost
        fields = ('id', 'donation_for', 'amount', 'country', 'state', 'latitude', 'longitude', 'end_date', 'received_amount', 'created_at', 'user', 'user_details', 'is_complete')


class DonationPostRequestSerializer(serializers.Serializer):
    donation_for = serializers.CharField(required=True)
    amount = serializers.FloatField(required=True)
    country = serializers.CharField(required=True)
    state = serializers.CharField(required=True)
    end_date = serializers.DateField(required=True)
    # user_id = serializers.IntegerField(required=True)


class DonationLogSerializer(serializers.ModelSerializer):
    donor_details = UserSerializer(
        read_only=True,
    )

    donation_details = DonationPostSerializer(
        read_only=True,
    )

    class Meta:
        model = DonationLog
        fields = ('id', 'amount', 'donation_post', 'donation_details', 'created_at', 'donor', 'donor_details')


class CreateDonationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationLog
        fields = '__all__'


class DonationLogRequestSerializer(serializers.Serializer):
    donation_post = serializers.IntegerField(required=True)
    amount = serializers.FloatField(required=True)
