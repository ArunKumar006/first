from rest_framework import generics, permissions,status
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer,UpdateUserSerializer,UserDataSerializer
from django.contrib.auth import login
from .serializers import ChangePasswordSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView 
from django.contrib.auth.models import User
from rest_framework.generics import UpdateAPIView
from django.shortcuts import render, get_object_or_404
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from django.contrib import auth
from django.http import Http404
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import viewsets
from django.contrib.auth.decorators import permission_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import TokenAuthentication
from apps.permissions import UpdateOwnProfile,DeleteOwbProfile



#from .permissions import IsAdminUser, IsLoggedInUserOrAdmin, IsAdminOrAnonymousUser

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes =[AllowAny,]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })
       

       
    def pre_save(self, obj):
        obj.owner = self.request.user
      
class UserAPI(generics.RetrieveAPIView):
    permission_classes =[IsAdminUser,]
    serializer_class =  UserSerializer
    def get_object(self,pk):
        try:

            return User.objects.get(pk=pk)
        except:
            raise Http404
    def get(self,request,pk,format=None):
        userData=self.get_object(pk)
        serializer=UserDataSerializer(userData)
        return Response(serializer.data)
    

    def delete(self,request,pk,format=None):
        userData=self.get_object(pk)
        userData.delete()
        return Response({'message':"user deleted"})
    


              
    
   
      
    
        

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
        
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UpdateProfileView(generics.UpdateAPIView):
     permission_classes = [IsAuthenticated,UpdateOwnProfile]

     queryset = User.objects.all()
     authentication_classes=[TokenAuthentication]
     
     serializer_class = UpdateUserSerializer
     
     
        

class userDetails(APIView):
    permission_classes =[IsAuthenticated,DeleteOwbProfile]
    authentication_classes=[TokenAuthentication]
    def get_object(self,pk):
        try:
            return User.objects.get(pk=pk)
        except:
            raise Http404
        
    def get(self,request,pk,format=None):
        userData=self.get_object(pk)
        serializer=UserDataSerializer(userData)
        return Response(serializer.data)
    
   
    def delete(self,request,pk,format=None):
        userData=self.get_object(pk)
        userData.delete()
        return Response({'message':"user deleted"})

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer    
    def get_object(self):
        
        return self.request.user
        self.response(User.first_name)

class AdminuserDetails(APIView):
    permission_classes = (IsAdminUser,)
   


    def get_object(self,pk):
        try:
            return User.objects.get(pk=pk)
        except:
            raise Http404
       
        user=self.request.user
       
   
    def get(self,request,pk,format=None):
       
        user=self.request.user
        
        userData=self.get_object(pk)
        serializer=UserDataSerializer(userData)
        return Response(serializer.data)
      

    def delete(self,request,pk,format=None):
        userData=self.get_object(pk)
        userData.delete()
        return Response({'message':"user deleted"})



from push_notifications.models import APNSDevice, GCMDevice

def new(request):
    userinfo = request.user
 
    print(userinfo)
 #reg = 'd4V2mO8ARx8:APA91bF0-9ua-3TYF-ILb8xjCVOJSd8xRc7sMsjZHCgvjQdLbrgi_ohzZHDzqxy7B1SLRP5Mb10GQZE8bTQv7ouFB9UJeNnGHpdFhqny3lbHijTlPSPrVdUsaBXyn6aYH8ImLe4MYrE-'
    device = GCMDevice.objects.all()
    print(device)
    device.send_message("Hello good evening!")
 
    return render(request,'new.html')
def newer(request):
    userinfo = request.user
 
    print(userinfo)
    device = GCMDevice.objects.filter(user_id__in=[1,3])
    print(device)
    device.send_message("hello")
    return JsonResponse("success",safe=False)