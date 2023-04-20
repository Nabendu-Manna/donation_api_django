from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets

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
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        serializer = HomePageLayoutSerializer(donationPost)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
