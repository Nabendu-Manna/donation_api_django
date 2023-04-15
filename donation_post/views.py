from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.models import User
from geopy.geocoders import Nominatim
from rest_framework import status, viewsets

from donation_post.serializers import DonationPostRequestSerializer, DonationPostSerializer

class DonationPostView(APIView):
    def post(self, request, *args, **kwargs):
        requestSerializer = DonationPostRequestSerializer(data = request.data)
        print(requestSerializer.is_valid())
        if not requestSerializer.is_valid():
            return Response(requestSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=request.data["user_id"])

        loc = Nominatim(user_agent="GetLoc")
        getLoc = loc.geocode(request.data["state"] + ", " + request.data["country"],)

        payload = {
            "donation_for": request.data["donation_for"],
            "amount": request.data["amount"],
            "country": request.data["country"],
            "state": request.data["state"],
            "latitude": str(getLoc.latitude),
            "longitude": str(getLoc.longitude),
            "end_date": request.data["end_date"],
            "user": request.data["user_id"]
        }
        serializer = DonationPostSerializer(data = payload)
        if serializer.is_valid():
            donationPost = serializer.save()
            return Response({"post_id": donationPost.id, "massage": "Successfully Created."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
