from rest_framework import serializers
from .models import User
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import User
from rest_framework.response import Response
from django.core.exceptions import ValidationError

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['email', 'username', 'password','password2','is_active','is_staff','is_connected']
        extra_kwargs={
            'password':{'write_only':True}
        }
    def save(self):
        if self.validated_data['password'] != self.validated_data['password2']:
            raise serializers.ValidationError({
                    'response':'success',
                    'error_message': 'provide same password detail for both the fields'
                    })

        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            password=self.validated_data['password']
        )
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type':'password'},write_only=False,required=True)
    
    def update(self):
        try:
            try:
                users_detail= User.objects.get(email=self.validated_data["email"])
            except Exception:
                raise Exception("user no match")
            users_detail.email
            is_connected = users_detail.is_connected
            password = users_detail.password
            response_data = {}
            if password == self.validated_data.get("password"):
                    if is_connected:
                        response_data["reponse"] = "success"
                        response_data["response_message"] = "user already connected."
                        response_data["error_message"] = "no error"
                    else:
                        try:
                            User.objects.filter(email=self.validated_data["email"]).update(is_connected=True)
                        except Exception as e:
                            raise Exception("status update for connection failed")
                        response_data["reponse"] = "success"
                        response_data["response_message"] = "successfully logged in."
                        response_data["error_message"] = "no error."
                    return response_data
            else:
                raise Exception("invalid password")
        except Exception as e:
            raise serializers.ValidationError({
                    "response":"failed",
                    "reponse_message":"no message.",
                    "error_message": str(e)
        })
class LogoutSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(style={'input_type':'password'},write_only=False,required=True)

    def update(self):
        response_data = {}
        try:
            try:
                users_data = User.objects.get(email=self.validated_data.get("email",""))
            except Exception:
                raise Exception("user no match")
            password = users_data.password
            if (self.validated_data.get("email","") == users_data.email) and (password == self.validated_data.get("password","")):
                if users_data.is_connected:
                    try:
                        User.objects.filter(email=self.validated_data["email"]).update(is_connected=False)
                    except Exception as e:
                        raise Exception("status update for connection failed")
                    response_data["reponse"] = "success"
                    response_data["response_message"] = "successfully logged out."
                    response_data["error_message"] = "no error."
                else:
                    response_data["reponse"] = "success"
                    response_data["response_message"] = "try logging in."
                    response_data["error_message"] = "no error."
                return response_data
            else:
                raise Exception("invalid password")
        except Exception as e:
            raise serializers.ValidationError({
                        "response":"failed",
                        "reponse_message":"no message.",
                        "error_message": "user no match"
            })