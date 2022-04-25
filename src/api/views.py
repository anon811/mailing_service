from rest_framework import viewsets
from .serializers import MailingSerializer, ClientSerializer
from .models import Mailing, Client


class MailingViewSet(viewsets.ModelViewSet):
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
