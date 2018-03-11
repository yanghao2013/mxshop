# _*_ coding:utf-8 _*_

__author__ = 'yanghao'
__date__ = '2018/1/9 22:44'

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
import re
from MxShop.settings import REGEX_MOBILE
from datetime import datetime,timedelta
from django.utils import timezone

from .models import VerifyCode

User = get_user_model()

class SmsSerializer(serializers.Serializer):

    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self,mobile):
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")
        if not re.match(REGEX_MOBILE,mobile):
            raise serializers.ValidationError("手机号码非法")

        one_minutes_age = timezone.now() - timedelta(hours=0,minutes=1,seconds=0)

        if VerifyCode.objects.filter(add_time__gt=one_minutes_age,mobile=mobile):
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile

class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化
    """
    class Meta:
        model = User
        fields = ('name','gender','birthday','email','mobile')


class UserRegSerializer(serializers.ModelSerializer):
    '''
    用户
    '''
    code = serializers.CharField(required=True,write_only=True,max_length=4,min_length=4,label='验证码',
                                 error_messages={
                                     "blank":'请输入验证码',
                                     "required":'请输入验证码',
                                     "max_length":'验证码格式错误',
                                     "min_length":'验证码格式错误',
                                 },
                                 help_text='验证码')

    username = serializers.CharField(required=True,allow_blank=False,label='用户名',
                                     validators=[UniqueValidator(queryset=User.objects.all(),message='用户已存在！')])

    password = serializers.CharField(label='密码',write_only=True,style={
        'input_type':'password'
    })
    # 作用于某个字段的验证
    def validate_code(self,code):
        verify_recodes = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if verify_recodes:
            last_record = verify_recodes[0]

            five_mintes_age = timezone.now() - timedelta(days=0,minutes=5,seconds=0)
            if five_mintes_age > last_record.add_time:
                raise serializers.ValidationError('验证码过期！')

            if last_record.code != code:
                raise serializers.ValidationError('验证码错误！')
        else:
            raise serializers.ValidationError('验证码错误！')

    # 可以用signal实现
    def create(self, validated_data):
        user = super(UserRegSerializer,self).create(validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    # 作用于全部字段的验证
    def validate(self,attrs): # attrs是所有字段验证完返回来的字段，code因为不是user的属性可以不返回
        attrs['mobile'] = attrs['username']
        del attrs['code']

        return attrs

    class Meta:
        model = User
        fields = ('username','code','mobile','password')

