from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.urls import reverse
from django.db.models import Q
from datetime import datetime
import stripe

from accounts.models import User
from geopy.geocoders import Nominatim
from rest_framework import status, viewsets
from donation_post.models import DonationLog, DonationPost
from donation_api.settings import STRIPE_SECRET_KEY

from rest_framework.permissions import IsAuthenticated
from donation_post.pagination import MyPageNumberPagination
from donation_post.serializers import (
    DonationLogRequestSerializer, DonationLogSerializer, DonationPostRequestSerializer, DonationPostSerializer,
    CreateDonationLogSerializer
)


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
        donationPostList = [item for item in donationPostList if not item.is_complete]
        return donationPostList


class DonationPostView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            donationPost = DonationPost.objects.all()
            donationPost = [item for item in donationPost if not item.is_complete]
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
        try:
            address = request.data["address"] + ", " + request.data["state"] + ", " + request.data["country"]
            getLoc = loc.geocode(address)
            # getLoc = loc.geocode(request.data["state"] + ", " + request.data["country"] + ", " + request.data["country"],)
        except Exception as e:
            return Response({'massage': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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


# class DonateView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, *args, **kwargs):
#         requestSerializer = DonationLogRequestSerializer(data = request.data)
#         if not requestSerializer.is_valid():
#             return Response(requestSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         donation = get_object_or_404(DonationPost, id=requestSerializer.data["donation_post"])
#
#         if donation.is_complete or donation.is_expired:
#             return Response({"errors": "Donation is not activate yet."}, status=status.HTTP_400_BAD_REQUEST)
#
#         if request.user.id == donation.user:
#             return Response({"errors": "You are not authorized to donate to this post."},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#         payload = {
#             "donation_post": requestSerializer.data["donation_post"],
#             "amount": requestSerializer.data["amount"],
#             "donor": request.user.id
#         }
#         serializer = DonationLogSerializer(data=payload)
#         if serializer.is_valid():
#             donationPost = serializer.save()
#             return Response({"post_id": donationPost.id, "massage": "Successfully Created."}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DonateView(APIView):
    permission_classes = [IsAuthenticated]

    def _payment(self, amount, donation):
        stripe.api_key = STRIPE_SECRET_KEY

        session = stripe.checkout.Session.create(
            success_url=self.request.build_absolute_uri(reverse('success')) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=self.request.build_absolute_uri(reverse('cancel')),
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': int(amount * 100),  # Stripe uses amounts in cents
                        'product_data': {
                            'name': donation.donation_for,
                        },
                    },
                    'quantity': 1
                },
            ],
            mode='payment',
            metadata={
                'donation_id': donation.id,
                'email': self.request.user.email,
                'amount': amount,
                "donor_id": self.request.user.id
            },
            customer_email=self.request.user.email,
        )
        return session.url

    def post(self, request, *args, **kwargs):
        requestSerializer = DonationLogRequestSerializer(data=request.data)
        if not requestSerializer.is_valid():
            return Response(requestSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

        donation = get_object_or_404(DonationPost, id=requestSerializer.data["donation_post"])

        if donation.is_complete or donation.is_expired:
            return Response({"errors": "Donation is not activate yet."}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.id == donation.user:
            return Response({"errors": "You are not authorized to donate to this post."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            stripe_payment_url = self._payment(requestSerializer.data["amount"], donation)
            return Response({'message': 'Success!', 'url': stripe_payment_url})
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PaymentSuccessView(APIView):

    def get(self, request):
        session_id = request.GET.get('session_id')
        stripe.api_key = STRIPE_SECRET_KEY
        if session_id:
            session = stripe.checkout.Session.retrieve(session_id)
            payment_intent = stripe.PaymentIntent.retrieve(session.payment_intent)
            payload = {
                "transaction_id": payment_intent.id,
                "amount": session.metadata.get('amount', '0'),
                "donor": session.metadata.get('donor_id', ''),
                "donation_post": session.metadata.get('donation_id', ''),
                "created_at": datetime.now(),
            }
            serializer = CreateDonationLogSerializer(data=payload)
            if serializer.is_valid():
                serializer.save()
            return render(request, 'payment_success.html', {'payload': serializer.data})
        else:
            return render(request, 'payment_cancel.html', {'error_message': 'Invalid session ID'})


class PaymentCancelView(APIView):

    def get(self, request):
        return render(request, 'payment_cancel.html')

