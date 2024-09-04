from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from .serializers import *
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth
from rest_framework.decorators import api_view,permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .renderers import Userrenderer

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponse
# Create your views here.


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self,attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k,v in serializer.items():
            data[k]=v
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user,many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    user = User.objects.all()
    serializer = UserSerializer(user,many=True)
    return Response(serializer.data)



class registeruser(GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (Userrenderer,)
    def post(self,request):
        data = request.data
        try:
            user = User.objects.create(first_name=data['first_name'],last_name=data['last_name'],username=data['username'],email=data['email'],password=make_password(data['password']))
            curren_site = get_current_site(request)
            email_subject = 'Please activate your account'
            message = render_to_string("account_verification_email.html",{
                'user':user,
                'domain':curren_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = data['email']
            send_email = EmailMessage(email_subject,message,to=[to_email])
            send_email.send()
            serializer = UserSerializerWithToken(user,many=False)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        except:
            message = {'detailes':'User already Exist'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)



def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        return HttpResponse('Successfully Your Account is Created')
    else:
        return HttpResponse('Invalid activation link')
    


class PasswordResetEmail(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            curren_site = get_current_site(request)
            email_subject = 'Reset Your Password'
            message = render_to_string("reset_password_email.html",{
                'user':user,
                'domain':curren_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(email_subject,message,to=[to_email])
            send_email.send()
            return Response('Password Reset email has been sent to your address .',status=status.HTTP_200_OK)
        else:
            return Response('Account does not exit',status=status.HTTP_400_BAD_REQUEST)



class PasswordTokenCheckAPI(GenericAPIView):
    serializer_class = PasswordCheckTokenapi
    def get(self,request,uidb64,token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
        except(TypeError,ValueError,OverflowError,User.DoesNotExist):
            user = None

        if not default_token_generator.check_token(user,token):
            return Response({'error':'token is not valid'},status=status.HTTP_401_UNAUTHORIZED)
        return Response({'success':'successfully reset','uidb64':uidb64,'token':token},status=status.HTTP_200_OK)


class SetNewpassword(GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    def patch(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response('Password Reset Success',status=status.HTTP_200_OK)



# class Register(APIView):
#     def post(self,request):
#         serializer = UserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    

# class LoginView(APIView):
#     def post(self,request):
#         email = request.data['email']
#         password = request.data['password']
#         user = User.objects.filter(email=email).first()
#         user = auth.authenticate(email=email,password=password)
#         if user is None:
#             raise AuthenticationFailed('User not found')
        
#         if not user.check_password(password):
#             raise AuthenticationFailed('incorrect password')
        

#         payload = {
#             'id':user.id,
#             'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
#             'iat': datetime.datetime.utcnow()
#         }

#         token = jwt.encode(payload, 'secret', algorithm='HS256')

#         response = Response()



#         response.set_cookie(key='jwt',value=token,httponly=True)

#         response.data = {
#             'jwt':token
#         }

#         return response
    


# class UserView(APIView):
#     def get(self,request):
#         token = request.COOKIES.get('jwt')
#         if not token:
#             raise AuthenticationFailed('UnAuthenticated!')
#         try:
#             payload = jwt.decode(token,'secret',algorithms=['HS256'])

#         except jwt.ExpiredSignatureError:

#             raise AuthenticationFailed('UnAuthenticated!')
        
#         user = User.objects.filter(id=payload['id']).first()
#         serializer = UserSerializer(user)
#         return Response(serializer.data)
    

# class LogoutView(APIView):
#     def post(self,request):
#         response = Response()
#         response.delete_cookie('jwt')
#         response.data ={
#             'message':'success'
#         }
#         return response
