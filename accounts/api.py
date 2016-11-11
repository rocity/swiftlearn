from .models import Account, Conversation
from .serializers import AccountSerializer, MessageSerializer
from rest_framework import views, status, permissions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404

from braces.views import LoginRequiredMixin

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

class MessageAPI(LoginRequiredMixin, ViewSet):
    serializer_class = MessageSerializer

    def list(self, request, format=None):
        return Response({}, status=200)

    def create_message(self, request, **kwargs):
        conversation_id = kwargs.get('conversation_id')
        conversation_qs = Conversation.objects.filter(users__in=[self.request.user])
        conversation = get_object_or_404(conversation_qs, pk=conversation_id)

        serializer = MessageSerializer(data=dict(
                                        conversation=conversation.id,
                                        sender=self.request.user.id,
                                        body=request.data['body'],
                                        ))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)