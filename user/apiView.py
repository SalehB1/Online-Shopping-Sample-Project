from rest_framework import generics
from .models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import ClientRegisterSerializer, GetTokenForLoginSerializer, ClientProfileSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404


# Create your viewApis here.

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
