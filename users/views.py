from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from .permissions import IsUserAddressOwner


class UserRegisterView(GenericAPIView):
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


class AddressViewSet(ReadOnlyModelViewSet):
    """
    List and Retrieve user addresses
    """

    permission_classes = (IsUserAddressOwner,)
    serializer_class = AddressReadOnlySerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
