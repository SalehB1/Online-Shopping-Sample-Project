import base64
from datetime import datetime
from random import sample

import pyotp
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import ClientRegisterSerializer, GetTokenForLoginSerializer, ClientProfileSerializer, \
    GenerateOtpLoginSerializer, LoginUserWithOtpSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
import os
import environ
from aiohttp import ClientSession
import asyncio
from rest_framework.views import APIView


# Create your viewApis here.
async def send_otp(phone, otp):
    async with ClientSession() as session:
        unit_url = "https://RestfulSms.com/api/Token"
        validation_headers = {'content-type': 'application/json'}
        validation_body = {"SecretKey": os.environ.get(
            'SECURITY_CODE'), "UserApiKey": os.environ.get('API_KEY')}
        response = await session.post(unit_url, json=validation_body, headers=validation_headers)
        if response.status != 201:
            return False
        data1 = await response.json()
        sending_sms_url = "http://RestfulSms.com/api/VerificationCode"
        sms_body = {"Code": otp, "MobileNumber": phone}
        headers_sms = {'content-type': 'application/json',
                       "x-sms-ir-secure-token": data1["TokenKey"]}
        response = await session.post(sending_sms_url, json=sms_body, headers=headers_sms)
        if response.status != 201:
            return False
        return await response.json()


class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.now()) + pyotp.random_hex()


class generationOtp:
    def create_otp(self, phone):
        keygen = pyotp.random_hex()
        key = base64.b32encode(keygen.encode())
        self.totp = pyotp.TOTP(key, interval=300)
        return self.totp.now()


sample = generationOtp()


class ClientRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ClientRegisterSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        return Response({"موفقیت": "ثبت نام شما با موفقیت انجام شد"}, status=status.HTTP_201_CREATED)


class GetTokenForLoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = GetTokenForLoginSerializer
    parser_classes = (MultiPartParser, FormParser)


class ClientProfileView(generics.RetrieveUpdateAPIView):
    http_method_names = ['put', 'get']
    permission_classes = (IsAuthenticated,)
    serializer_class = ClientProfileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)


class ClientOtpGenerator(APIView):

    def post(self, request):
        if 'phone' in request.data:
            serializer = GenerateOtpLoginSerializer(data=request.data)
            isvalid = serializer.is_valid(raise_exception=True)
            if isvalid:
                user_obj = get_object_or_404(
                    User, phone=request.data["phone"])
                totp = sample.create_otp(user_obj.phone)
                loop = asyncio.new_event_loop()
                data = loop.run_until_complete(send_otp(user_obj.phone, totp))
                if data:
                    return Response({"Success": "user successfuly registered.", "otp": totp},
                                    status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)


class ActivateUserPhone(APIView):

    def post(self, request):
        if 'phone' not in request.data or 'otp' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, phone=request.data["phone"])
        try:
            if sample.totp.verify(request.data["otp"]):

                user_obj = get_object_or_404(User, phone=user.phone)
                if user_obj.is_verified:
                    return Response({'msg': 'user already registered'}, status=status.HTTP_403_FORBIDDEN)
                user_obj.is_verified = True
                user_obj.save()
                return Response({'msg': 'user successfuly registered'}, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'msg': 'OTP Wrong !'}, status=status.HTTP_400_BAD_REQUEST)


class LoginWithOtp(APIView):
    def post(self, request):
        if 'phone' not in request.data or 'otp' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = LoginUserWithOtpSerializer(data=request.data)
        isvalid = serializer.is_valid(raise_exception=True)
        if isvalid:
            user_obj = get_object_or_404(
                User, phone=request.data["phone"])
            if user_obj and sample.totp.verify(request.data["otp"]) and user_obj.is_verified == True:
                refresh = RefreshToken.for_user(user_obj)

                return Response({'msg': 'Login Success', 'access': str(refresh.access_token)},
                                status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'you dont have permision to login please register your phone '},
                                status=status.HTTP_200_OK)

        return Response({"message": "your field is worng."}, status=status.HTTP_400_BAD_REQUEST)
