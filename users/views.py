from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from .permissions import IsUserAddressOwner


class UserRegisterView(GenericAPIView):
    """
    Register a new user

    Args:
        request (Request): The HTTP request object

    Returns:
        Response: The HTTP response object with the serialized data and status code
    """

    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        user = self.request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserRetrieveView(RetrieveAPIView):
    """
    Get user details
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


class AddressViewSet(ModelViewSet):
    """
    List and Retrieve user addresses
    """

    permission_classes = (IsUserAddressOwner,)

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return AddressWriteSerializer
        return AddressReadOnlySerializer
