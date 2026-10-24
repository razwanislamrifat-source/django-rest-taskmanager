from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
from .serializers import RegisterSerializer


class RegisterAnonThrottle(AnonRateThrottle):
    scope = 'register'


class RegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [RegisterAnonThrottle]
    serializer_class = RegisterSerializer
