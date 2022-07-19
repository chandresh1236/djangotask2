from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer
import io
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@csrf_exempt
# @permission_classes([IsAuthenticated])
@api_view(["POST"])
def signupView(request):
    if request.method == 'POST':
        data = request.data
        #data = JSONParser().parse(json_data)
        serializer = RegisterSerializer(data=request.data)
       
        resp_data = {}
        if serializer.is_valid():
            print(serializer.data)
            serializer.save()
            resp_data['response']='successfully created'
            resp_data['email']= data['email']
            resp_data['username']= data['username']
            return Response(resp_data,status=201)
        return Response(serializer.errors,status=400)

@api_view(["POST"])
@csrf_exempt
# @permission_classes([IsAuthenticated])
def loginView(request):
    if request.method == 'POST':
        login_serializer = LoginSerializer(data=request.data)
        if login_serializer.is_valid():
            response_data = login_serializer.update()
            if response_data:
                return Response(response_data,status=201)
        return Response(login_serializer.errors,status=400)


@api_view(["POST"])
@csrf_exempt
# @permission_classes([IsAuthenticated])
def logOut(request):
    if request.method == 'POST':
        logout_serializer = LogoutSerializer(data=request.data)
        if logout_serializer.is_valid():
            response_details = logout_serializer.update()
            if response_details:
                return Response(response_details,status=201)
        return Response(logout_serializer.errors,status=400)