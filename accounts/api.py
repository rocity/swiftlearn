from .models import Account
from .serializers import AccountSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings
from django.contrib.auth import login


class SignUpAPI(APIView):

    serializer_class = AccountSerializer
  
    def post(self, request, format=None):
        serializer = self.serializer_class( data =request.data)
        if serializer.is_valid():
            serializer.save()
            
            user = Account.objects.get(email=serializer.data['email'])
            user.backend = settings.AUTH_BACKEND
            login(self.request, user)
            
            return Response("success", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        