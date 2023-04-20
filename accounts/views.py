from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from accounts.models import User

from accounts.serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout as djLogout

from django.core.mail import send_mail
from donation_api import settings

import random
import string

from django.utils.translation import gettext_lazy as _


# Create your views here.
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response(
                {"user_id": user.id, "token": token.key}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        user = authenticate(
            username=request.data["email"], password=request.data["password"]
        )
        if not user:
            return Response(
                {"error": "Invalid credential."}, status=status.HTTP_400_BAD_REQUEST
            )
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response(
            {"user_id": user.id, "token": token.key}, status=status.HTTP_200_OK
        )


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            djLogout(request)
            return Response(
                {"message": "Logout Successful."}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "You are not Logged in. Please Login and try again."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ForgotPassword(APIView):
    def post(self, request, *args, **kwargs):
        if not request.data["email"]:
            return Response(
                {"error": "Invalid credential."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if User.objects.filter(email=request.data["email"]).count() == 0:
            return Response(
                {"error": "Email not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        characters = string.ascii_letters + string.digits + "@#$&%"
        password = "".join(random.choice(characters) for i in range(12))

        user = User.objects.get(email=request.data["email"])
        user.set_password(password)
        user.save()

        send_mail(
            "Subject here",
            "Your new password is " + password,
            "settings.EMAIL_HOST_USER",
            ["mannanabendu2000@gmail.com", request.data["email"]],
            fail_silently=False,
        )

        return Response(
            {"message": "New password has been sent to your email."},
            status=status.HTTP_200_OK,
        )

@api_view(['GET'])
def isUserValid(request):
    if request.user.is_authenticated:
        return Response({"valid": True}, status=status.HTTP_200_OK)
    else:
        return Response({"valid": False}, status=status.HTTP_200_OK)


@api_view(['GET'])
def isAdminValid(request):
    if request.user.is_authenticated and request.user.role == 0:
        return Response({"valid": True}, status=status.HTTP_200_OK)
    else:
        return Response({"valid": False}, status=status.HTTP_200_OK)
