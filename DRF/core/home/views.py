from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class LoginAPI(APIView):
    def post(self,request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors
            },status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=serializer.data['username'],password=serializer.data['password'])
        if not user:
            return Response({
                'status': False,
                'message': "Invalid Credential"
            },status.HTTP_400_BAD_REQUEST)

        token,_ = Token.objects.get_or_create(user=user)

        return Response({
            'status': True,
            'message': "Login Succesfull",
            'Token': str(token)
        },status.HTTP_201_CREATED)
        


class RegisterAPI(APIView):

    def post(self,request):
        data = request.data
        serializers = RegisterSerializer(data=data)


        if not serializers.is_valid():
            return Response({
                'status': False,
                'message': serializers.errors
            },status.HTTP_400_BAD_REQUEST)
        serializers.save()

        return Response({
            'status': True,
            'message': "User Created"
        },status.HTTP_201_CREATED)

class PersonAPI(APIView):

    def get(self,request):
        objs = Person.objects.filter(color__isnull=False)
        serializer = PeopleSerializer(objs, many = True)
        return Response(serializer.data)
    
    def post(self,request):
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def put(self,request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PeopleSerializer(obj,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def patch(self,request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PeopleSerializer(obj,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self,request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete()
        return Response({"message": "Person Record Deleted"})



@api_view(['GET','POST'])
def index(request):
    courses = {
        'course_name' : 'Python',
        'learn' : ['Flask','Django','Tornado','FastApi'],
        'course_provider' : 'Scaler'
    }
    if request.method == 'GET':
        print(request.GET.get('search'))
        print("GET Method is called")
    elif request.method == 'POST':
        data = request.data
        print("POST Method is called")
        print("*************")
        print(data['name'])
        print(data['age'])
        print("*************")
    return Response(courses)

@api_view(['POST'])
def login(request):
    data = request.data
    print(data)
    serializer = LoginSerializer(data=data)

    if serializer.is_valid():
        data = serializer.validated_data
        return Response({'message':"success"})

    return Response(serializer.error_messages)



@api_view(['GET','POST','PUT','PATCH','DELETE'])
def person(request):
    if request.method == 'GET':
        objs = Person.objects.filter(color__isnull=False)
        serializer = PeopleSerializer(objs, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'PUT':
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PeopleSerializer(obj,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'PATCH':
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PeopleSerializer(obj,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    else:
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete()
        return Response({"message": "Person Record Deleted"})



class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()

    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith = search)
        serializer = PeopleSerializer(queryset,many=True)

        return Response({'status':200,'data':serializer.data},status=status.HTTP_200_OK)