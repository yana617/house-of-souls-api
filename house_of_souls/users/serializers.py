from django.contrib.auth import get_user_model
from rest_framework import serializers
from utils.factories_utils import extra_kwargs_factory


User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'phone',
            'password',
        )
        extra_kwargs = extra_kwargs_factory(
            ('password',),
            required=True,
            allow_null=False,
            write_only=True
        )

    def validate(self, data):
        phone = data.get('phone', None)

        if phone is None:
            raise serializers.ValidationError('phone should be provided')

        user = User.objects.filter(phone=phone).first()
        if user is None or not user.check_password(data['password']):
            raise serializers.ValidationError('No user with such credentials')
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        required_fields = (
            'phone',
            'name',
            'surname',
            'password',
            'birthday',
        )
        fields = required_fields + (
            'id',
            'date_joined',
            'is_volunteer',
            'is_admin',
            'last_login',
        )
        extra_kwargs = extra_kwargs_factory(
            required_fields,
            required=True,
            allow_null=False
        )
        read_only_fields = ('date_joined', 'is_volunteer', 'is_admin', 'last_login',)
        extra_kwargs.update(extra_kwargs_factory(('password', ), write_only=True))

    def create(self, validated_data):
        return User.objects.create_user(
            validated_data.pop('phone'),
            validated_data.pop('password'),
            **validated_data
        )
