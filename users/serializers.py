from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import  RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator



class UserSerializer(serializers.ModelSerializer):
    isadmin = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email','isadmin']

    def get_isadmin(self,obj):
        return obj.is_staff

class UserSerializerWithToken(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isadmin = serializers.SerializerMethodField(read_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id','_id','username','fullname','email','isadmin','token']



    def get_fullname(self,obj):
        firstname = obj.first_name
        lastname = obj.last_name
        fullname =str(lastname)
        if fullname==' ':
            fullname = 'Create FullName'
        return None

    def get__id(self,obj):
        return obj.id
    
    def get_isadmin(self,obj):
        return obj.is_staff
    
    def get_token(self,obj):
         token = RefreshToken.for_user(obj)
         return str(token.access_token)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password']




class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=2)
    class Meta:
        model = User
        fields = ['email']

class PasswordCheckTokenapi(serializers.ModelSerializer):
    token = serializers.CharField(min_length=1,write_only=True)
    uidb64 = serializers.CharField(min_length=1,write_only=True)

    class Meta:
        model = User
        fields = ['token','uidb64']



class SetNewPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68,min_length=6,write_only=True)
    token = serializers.CharField(min_length=1,write_only=True)
    uidb64 = serializers.CharField(min_length=1,write_only=True)

    class Meta:
        model = User
        fields = ['password','token','uidb64']


    def validate(self,attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
            if not default_token_generator.check_token(user,token):
                raise AuthenticationFailed('the reset link is invalid',401)
            user.set_password(password)
            user.save()
            return user

        except Exception as e:
            raise AuthenticationFailed('The Reset Link is Invalid',401)
        return super().validate(attrs)
    


        # password = request.POST['password']
        # confirm_password = request.POST['confirm_password']
        # if password == confirm_password:
        #     uid = request.session.get('uid')
        #     user = Account.objects.get(pk=uid)
        #     user.set_password(password)
        #     user.save()
        #     messages.success(request,'Password Reset Successfull')
        #     return redirect('login')
        # else:
        #     messages.error(request,'Password do not match')
        #     return redirect('resetpassword')
