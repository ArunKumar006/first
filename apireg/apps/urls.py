from .views import RegisterAPI,ChangePasswordView,UpdateProfileView
from django.urls import path
from .views import MyObtainTokenPairView
from knox import views as knox_views
from .views import  UserAPI
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authtoken.views import obtain_auth_token
from apps import views
from django.contrib.auth.decorators import permission_required
from rest_framework.permissions import AllowAny,IsAdminUser
schema_view = get_schema_view(
    openapi.Info(
        title="User API ",
        default_version='v1',
        description="An api for user",
        terms_of_service="https://yourco/terms/",
        contact=openapi.Contact(email="contact@contacts.remote"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)
    
   
urlpatterns = [
    path('Login/',obtain_auth_token,name="login"),
    path('new/',views.new,name="new"),
   # path('AdminLogin/',obtain_auth_token,name="loginAdmin"),
    #path('AdminuserDetails/<int:pk>/',views.userDetails.as_view(),name="userDetails"),
    path('userDetails/<int:pk>/',views.userDetails.as_view(),name="userDetails"),
    #path('Logout/',views.LoginViewSet, name='logout'),
    #path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('Register/', RegisterAPI.as_view(), name='register'),
    path('Adminuserdetails/<int:pk>/', UserAPI.as_view()),
    path('Update_profile/<int:pk>/', UpdateProfileView.as_view(), name='auth_update_profile'),
    #path('Password-change/', ChangePasswordView.as_view(), name='change-password'),
    path('', schema_view.with_ui('swagger',
                                 cache_timeout=0), name='schema-swagger-ui'),
    path("redoc", schema_view.with_ui('redoc',
                                      cache_timeout=0), name='schema-redoc'),

] 
