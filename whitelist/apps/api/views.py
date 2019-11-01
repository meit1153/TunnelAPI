from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import parsers, renderers
from .serializer import AuthTokenSerializer, AssignedPortSerializer, AddAssignedPortSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from .models import UserKey, AssignPort
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import login, authenticate
from .utils import find_free_port

# Create your views here.

class LoginView(APIView):
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    api_view = ['POST']

    def post(self, request, format=None):
        try:
            try:
                serializer = AuthTokenSerializer(data=request.data)
                serializer.is_valid(raise_exception = True)

                key = serializer.validated_data['key']
            
                data = UserKey.objects.get(key=key)
            except:
                return Response({'error': 'Please enter valid user key'}, status=status.HTTP_400_BAD_REQUEST)
            user = data.user
            token, created = Token.objects.get_or_create(user=user)
            context = {
                    'token' : token.key,
                    'success': 'Successfully Logged In'
            }
            return Response(context, status = status.HTTP_200_OK)
        except:
            return Response({'error': 'Something went wrong, please try again or contact administrator'}, status=status.HTTP_400_BAD_REQUEST)

class AvailablePort(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated,]
    api_view = ['GET']

    def get(self,request, format=None):
        try:

            port_no = find_free_port()
        except:
            return Response(dict({"error":"There is no free port available"}), status=status.HTTP_404_NOT_FOUND)

        return Response(dict({"available_port " : port_no}), status=status.HTTP_200_OK)

class AssignedPort(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated,]
    api_view = ['GET', 'POST', 'PUT']

    def get(self,request, format=None):
        try:
            HTTP_AUTHORIZATION = request.META.get('HTTP_AUTHORIZATION', '')
            token = HTTP_AUTHORIZATION.split(' ')
            user =  Token.objects.get(key=token[1])
            assigned_port = AssignPort.objects.filter(user_id=user.user_id)
            data = []

            for assigned in assigned_port:
                context = {
                    "user": assigned.user.username,
                    "assigned_port" : assigned.assigned_port,
                    "user_ip" : assigned.user_ip,
                    "user_port" : assigned.user_port
                }
                data.append(context)

        except:
            return Response(dict({"assinged_port":"There is no port assigened to user"}), status=status.HTTP_404_NOT_FOUND)

        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request):
        try:
            HTTP_AUTHORIZATION = request.META.get('HTTP_AUTHORIZATION', '')
            token = HTTP_AUTHORIZATION.split(' ')
            user =  Token.objects.get(key=token[1])
            data = request.data
            data = data.dict()
            post_instance = AssignPort.objects.create(user= user.user, assigned_port=data['assigned_port'], user_ip=data['user_ip'], user_port=data['user_port'])
            
            return Response({"success": "Successfully assinged port"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": "Something went wrong, Please try again later"},
                            status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, format=None):
        try:
            assigned_port = request.data.get('assigned_port', None)
            assigned = AssignPort.objects.get(assigned_port= assigned_port).delete()
            return Response(dict({"success": "Assigned port is deleted"}), status=status.HTTP_200_OK)
        except:
            return Response(dict({"error": "Something went wrong, please try again"}),status=status.HTTP_400_BAD_REQUEST)