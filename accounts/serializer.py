from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password')
        extra_kwargs = {'password':{'write_only': True},}

    def create(self, validated_data):
        # psql velu anna
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style = { 'input_type': 'password' } , trim_whitespace= False,)

    def validate(self,data):
        username = data.get('username')
        password = data.get('password')
        if username and password :
            if User.objects.filter(username=username).exists():
                print(username, password)
                # psql velu anna
                user = authenticate(request = self.context.get('request'),  = username, password= password)
            else:
                msg = {
                    'detail': 'username number not found',
                    'status': False,
                }
                raise serializers.ValidationError(msg)
            if not user:
                msg = {
                    'detail' : 'username number and password are not matched',
                    'status' : False,
                    'phone' : username
                }
                raise serializers.ValidationError(msg,code='authencation is user')
        else:
            msg = {
                'detail': 'username number and password are not sent',
                'status': False,
                'phone': username
            }
            raise serializers.ValidationError(msg, code='Not registered')

        data['user'] = user
        return data
