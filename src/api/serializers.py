from rest_framework import serializers
from .models import Mailing, Client, Message


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = ['id', 'start_datetime', 'stop_datetime', 'text', 'mobile_operator_code',
                  'tag', 'messages_sent', 'messages_scheduled', 'messages_error', 'message_failed']

        extra_kwargs = {
            'messages_sent': {'read_only': True},
            'messages_scheduled': {'read_only': True},
            'messages_error': {'read_only': True},
            'message_failed': {'read_only': True},
        }


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'phone_number', 'tag', 'timezone', 'mobile_operator_code']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'dispatch_datetime', 'status', 'mailing', 'clients']