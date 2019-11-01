from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import parsers, renderers
from .serializer import AuthTokenSerializer, AssignedPortSerializer, AddAssignedPortSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from .models import UserKey, AvailablePort, AssignPort
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import login, authenticate

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



class AssignedPort(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated,]
    api_view = ['GET', 'POST', 'PUT']

    def get(self,request, format=None):
        try:
            assigned_port = AssignPort.objects.filter(user=reques.user).order_by('date_added')
            serialized = AssignedPortSerializer(assigned_port)
        except:
            return Response(dict({"assinged_port":["There is no port assigened to user"]}), status=status.HTTP_404_NOT_FOUND)

        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        try:
            user = request.user
            data = request.data

            port_assigned = AvailablePort.objects.filter(is_available=True).order_by('portno').first()
            data['assigned_port'] = port_assigned
            data['user'] = user

            serialized = AddAssignedPortSerializer(data=data)
            if serialized.is_valid():
                serialized.save()
            else:
                return Response({"error": [str(serialized.errors)]}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"success": "Successfully assinged port"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": "Something went wrong, Please try again later"},
                            status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, format=None):
        try:
            assigned_port = request.data.get('assigned_port', None)
            assigned = AssignPort.objects.get(assigned_port__portno = assigned_port)
            try:
                assigned.is_enable = False
                assigned.save()
            except:
                return Response(dict({"error": "Please provide a valid assigned port number"}),status=status.HTTP_400_BAD_REQUEST)
            return Response(dict({"success": "Status is successfully updated for assigned port."}), status=status.HTTP_200_OK)
        except:
            return Response(dict({"error": "Something went wrong, please try again"}),status=status.HTTP_400_BAD_REQUEST)