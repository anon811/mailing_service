from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MailingViewSet, ClientViewSet
from .yasg import swaggerurlpatterns


router = DefaultRouter()

router.register(r'mailings', MailingViewSet)
router.register(r'clients', ClientViewSet)

urlpatterns = [
    path('api/', include(router.urls))
]

urlpatterns += swaggerurlpatterns
