from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from .models import Account

from django.contrib.auth import get_user_model


class AccountSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        validators=[
        UniqueValidator(
            queryset=Account.objects.all(),
            message="This email is already Exist!.",
            )]
        )

    password = serializers.CharField()

    confirm_password = serializers.CharField(
        write_only=True,
        )
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = Account
        fields = ('email','first_name', 'last_name', 'password','confirm_password','user_type')
        write_only_fields = ('password',)

    def validate(self, data):
        if data.get('password')!= data.get('confirm_password'):
            raise serializers.ValidationError("Password didn't match. Try again.")
        return data
      

    def create(self, validated_data):
        email = validated_data.get('email')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        password = validated_data.get('password')
        user_type = validated_data.get('user_type')
        user = Account.objects.create(email=email,user_type=user_type,first_name=first_name,last_name=last_name)
        user.username = user._extract_username()
        user.set_password(password)
        user.save()
        user._send_confirmation_email() # activate account
        return user


class LoginSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(
        validators=[
        UniqueValidator(
            queryset=Account.objects.all(),
            message="This email is already Exist!.",
            )]
        )

    password = serializers.CharField()

    class Meta:
        model = Account
        fields = ('email', 'password')