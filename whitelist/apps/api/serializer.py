from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserKey, AssignPort, AvailablePort
from allauth.account.models import EmailAddress
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions

class AuthTokenSerializer(serializers.Serializer):
    key = serializers.CharField()

    def validate(self, attrs):
        key = attrs.get('key')
        if key:

            data = UserKey.objects.get(key=key)
            user = data.user
            if user and not EmailAddress.objects.filter(user=user, email=user.email, verified=True).exists():
                msg = _('Your Account is not verified')
                raise exceptions.ValidationError(msg)
            elif user:
                if not user.is_active:
                    msg = _('Your Account is disabled')
                    raise exceptions.ValidationError(msg)
            else:
                msg = _('Sorry, your key is not valid or incorrect, Please try again')
        
        else:
            msg = _('Please provide key to log in')
            raise exceptions.ValidationError(msg)

        attrs[user] = user
        return attrs


class AssignedPortSerializer(serializers.Serializer):
    
    class Meta:
        model = AssignPort
        field = ('user', 'key', 'assigned_port', 'user_ip', 'user_port', 'is_enable')

class AddAssignedPortSerializer(serializers.Serializer):

    class Meta:
        model = AssignPort