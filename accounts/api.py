from .models import Account
from .serializers import AccountSerializer, ProfileSerializer
from events.models import Event
from events.serializers import EventSerializer
from rest_framework import views, status, permissions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404



class SignUpAPI(views.APIView):

    serializer_class = AccountSerializer
  
    def post(self, request, format=None):
        serializer = self.serializer_class( data =request.data)
        if serializer.is_valid():
            serializer.save()
            
            user = Account.objects.get(email=serializer.data['email'])
            user.backend = settings.AUTHENTICATION_BACKENDS[0]
            login(self.request, user)
            
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(views.APIView):
    """API endpoint on Login
    """
    serializer_class = AccountSerializer

    def post(self, request, format=None):
        data = self.request.data
        email = data.get('email')
        password = data.get('password')
        account = authenticate(email=email, password=password)

        if account is not None:
            if account.is_active:
                login(request, account)
                serialized = AccountSerializer(account)
                return Response(serialized.data)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account has been  disabled.'
                    }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/Password combination invalid.'
                }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    """API endpoint on Logout
    """
    def post(self, request, format=None):
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class ProfileAPI(ViewSet):

    serializer_class = ProfileSerializer

    def detail(self, *args, **kwargs):
        user_id = kwargs.get('user_id')
        profile = get_object_or_404(Account, id=user_id) if user_id else self.request.user
        serializer = ProfileSerializer(profile)
        
        return Response(serializer.data)

    def update_profile(self, *args, **kwargs):
        profile = get_object_or_404(Account, email=self.request.user)
        serializer = ProfileSerializer(profile, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


        # event = get_object_or_404(Event, pk=kwargs.get('event_id'))
        # serializer = EventSerializer(event, data=self.request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        # return Response(serializer.errors)
