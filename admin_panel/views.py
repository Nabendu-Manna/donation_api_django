import datetime
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from accounts.permissions import IsUserAdmin

from admin_panel.models import HomePageLayout
from admin_panel.serializers import (
    HomePageLayoutRequestSerializer,
    HomePageLayoutSerializer,
)
import os


class HomePageLayoutView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            donationPost = HomePageLayout.objects.first()
            if donationPost is None:
                donationPost, crated = HomePageLayout.objects.get_or_create(
                    title = "Make a Difference Today. Donate in itowe.com",
                    body_text = "Welcome to our donation page! We are grateful for your interest in supporting our cause and making a positive impact in the world. We relies on the generosity of donors like you to fund our mission. Every dollar you donate goes directly towards supporting our programs and helping those in need. Whether you choose to give a one-time donation or become a monthly supporter, your contribution will make a difference in the lives of those we serve. Thank you for your support and for joining us in our efforts to make the world a better place. Together, we can make a difference!",
                    image = "/images/setting/bg.jpg",
                    created_at = datetime.datetime.now()
                )
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        serializer = HomePageLayoutSerializer(donationPost, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HomePageLayoutUpdateView(APIView):
    permission_classes = [IsUserAdmin]
    def patch(self, request, *args, **kwargs):
        homePageLayout = HomePageLayout.objects.first()
        if not homePageLayout:
            requestSerializer = HomePageLayoutRequestSerializer(data=request.data)
            if not requestSerializer.is_valid():
                return Response(
                    requestSerializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            payload = {
                "title": request.data["title"],
                "body_text": request.data["body_text"],
                "image": request.data["image"],
            }
            serializer = HomePageLayoutSerializer(data=payload)
        else:
            serializer = HomePageLayoutSerializer(
                instance=homePageLayout, data=request.data, partial=True
            )
        if serializer.is_valid():
            homePageLayout = serializer.save()
            if(request.data["image"]):
                if(homePageLayout.image and os.path.exists(homePageLayout.image.path)):
                    os.remove(homePageLayout.image.path)
                homePageLayout.image = request.data["image"]
                homePageLayout = serializer.save()
            return Response(
                {"post_id": homePageLayout.id, "massage": "Successfully Updated."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
