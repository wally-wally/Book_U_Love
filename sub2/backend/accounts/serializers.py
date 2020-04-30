from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework_jwt.settings import api_settings
from django.utils.translation import ugettext as _
from . import models
from api.serializers import MyReviewSerializer
User = get_user_model()

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = get_user_model()
        fields =['email', 'password', 'username' ,]
    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            age = validated_data['age'] if 'age' in validated_data else None,
            gender = validated_data['gender'] if 'gender' in validated_data else None,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, data):
        non_alpha = set([s for s in "!@#$%^&*()|-=_+\[]{};':\",./?><"])
        error = dict({'username' : [], 'email' : [],'password': []})
        if not 8 <= len(data['password']) < 16:   # password length error: 2
            error['password'].append('비밀번호를 8 ~ 16자로 작성해주세요!')
        if data['password'].isdigit():  # password is only numbers: 3
            error['password'].append('비밀번호를 다른 문자와 조합해주세요!')
        if get_user_model().objects.filter(email= data['email']): # same username in db : 4
            error['email'].append('중복된 email이 있습니다.')
        if get_user_model().objects.filter(username=data['username']):
            error['username'].append('중복된 username이 있습니다.')
        if not 0 < len(data['username']) < 16:  # username length error: 5 
            error['username'].append('username을 1 ~ 16 글자로 해주세요!')
        for word in data['username']: # non_alph in username: 6
            if word in non_alpha:
                error['username'].append('username에 특수문자를 넣지 말아주세요!')
                break
        return error
    
    def user_update(self, data):
        pass

class CustomJWTSerializer(JSONWebTokenSerializer):
    username_field = 'username'
    def validate(self, attrs):
        password = attrs.get("password")
        user_obj = User.objects.filter(email=attrs.get("username")).first() or User.objects.filter(username=attrs.get("username")).first()
        if user_obj is not None:
            credentials = {
                'username':user_obj.username,
                'password': password
            }
            if all(credentials.values()):
                user = authenticate(**credentials)
                if user:
                    if not user.is_active:
                        msg = _('User account is disabled.')
                        raise serializers.ValidationError(msg)

                    payload = jwt_payload_handler(user)
                    print({
                        'token': jwt_encode_handler(payload),
                        'user': user
                    })
                    return {
                        'token': jwt_encode_handler(payload),
                        'user': user
                    }
                else:
                    msg = _('Unable to log in with provided credentials.')
                    raise serializers.ValidationError(msg)

            else:
                msg = _('Must include "{username_field}" and "password".')
                msg = msg.format(username_field=self.username_field)
                raise serializers.ValidationError(msg)

class UserUpdateSerializer(serializers.ModelSerializer):
    categorys = serializers.SerializerMethodField()
    class Meta:
        model = models.User
        fields = ('username', 'email', 'gender', 'age', 'categorys')

    def get_categorys(self,obj):
        categorys = []
        for i in obj.favoriteCategory.all():
            categorys.append(i.name)
        return categorys

class UserSimpleSerializer(serializers.ModelSerializer):
    categorys = serializers.SerializerMethodField()
    r_cnt = serializers.SerializerMethodField()
    class Meta:
        model = models.User
        fields = ('username', 'email', 'gender', 'age', 'categorys', 'r_cnt')

    def get_categorys(self,obj):
        categorys = []
        for i in obj.favoriteCategory.all():
            categorys.append(i.name)
        return categorys

    def get_r_cnt(self,obj):
        return len(obj.review_set.all())

class UserDetailSerializer(serializers.ModelSerializer):
    categorys = serializers.SerializerMethodField()
    review_set = MyReviewSerializer(many=True)
    class Meta:
        model = models.User
        fields = ('username', 'email', 'gender', 'age', 'categorys', 'review_set')

    def get_categorys(self,obj):
        categorys = []
        for i in obj.favoriteCategory.all():
            categorys.append(i.name)
        return categorys


class UserUpdatePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('password',)