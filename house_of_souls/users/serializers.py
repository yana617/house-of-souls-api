from django.contrib.auth import get_user_model
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField


User = get_user_model()


def extra_kwargs_factory(fields, **options):
    return {k: options for k in fields}


class LoginSerializer(serializers.Serializer):
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


# class CustomerSerializer(serializers.ModelSerializer):
#     addition_info = serializers.SerializerMethodField()
#     token = serializers.SerializerMethodField()
#
#     class Meta:
#         model = User
#
#         required_fields = (
#             'username',
#             'email',
#             'password',
#         )
#
#         fields = required_fields + (
#             'id',
#             'date_joined',
#             'token',
#             'is_temporary',
#             'addition_info',
#         )
#         extra_kwargs = extra_kwargs_factory(
#             required_fields,
#             required=True,
#             allow_null=False
#         )
#         read_only_fields = ('date_joined', 'is_temporary',)
#         extra_kwargs.update(extra_kwargs_factory(('password', ), write_only=True))
#
#     def create(self, validated_data):
#         return User.objects.create_customer(
#             validated_data.pop('email').lower(),
#             validated_data.pop('password'),
#             **validated_data
#         )
