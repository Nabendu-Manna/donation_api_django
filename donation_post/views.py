from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.db.models import Q

from accounts.models import User
from geopy.geocoders import Nominatim
from rest_framework import status, viewsets
from donation_post.models import DonationPost

from rest_framework.permissions import IsAuthenticated
from donation_post.pagination import MyPageNumberPagination
from donation_post.serializers import DonationPostRequestSerializer, DonationPostSerializer


class DonationPostListView(ListAPIView):
    pagination_class = MyPageNumberPagination
    serializer_class = DonationPostSerializer
    def get_queryset(self, *args, **kwargs):
        search = self.request.query_params.get("search")

        if search is not None:
            user = User.objects.filter(Q(first_name__contains = search) | Q(last_name__contains = search))
            if(len(user) > 0):
                donationPostList = DonationPost.objects.filter(Q(donation_for__contains = search) | Q(user = user[0].id))
            else:
                donationPostList = DonationPost.objects.filter(Q(donation_for__contains = search))
        else:
            donationPostList = DonationPost.objects.all()
        return donationPostList


class DonationPostView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            donationPost = DonationPost.objects.all()
        except:
            return Response({}, status = status.HTTP_400_BAD_REQUEST)
        
        serializer = DonationPostSerializer(donationPost, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)


class DonationPostCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        requestSerializer = DonationPostRequestSerializer(data = request.data)
        if not requestSerializer.is_valid():
            return Response(requestSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # user = get_object_or_404(User, id=request.data["user_id"])

        loc = Nominatim(user_agent="GetLoc")
        getLoc = loc.geocode(request.data["state"] + ", " + request.data["country"] + ", " + request.data["country"],)

        payload = {
            "donation_for": request.data["donation_for"],
            "amount": request.data["amount"],
            "country": request.data["country"],
            "state": request.data["state"],
            "latitude": str(getLoc.latitude),
            "longitude": str(getLoc.longitude),
            "end_date": request.data["end_date"],
            "user": request.user.id
        }
        serializer = DonationPostSerializer(data = payload)
        if serializer.is_valid():
            donationPost = serializer.save()
            return Response({"post_id": donationPost.id, "massage": "Successfully Created."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DonateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        pass