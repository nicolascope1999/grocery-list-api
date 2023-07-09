""""
Views for the user api
"""
# handles the logic for requests and responses
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


# handles http post requests, only need to define the serializer and set it
# here and it will automatically create the view for us
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for the user."""
    # this is the serializer that will be used to generate the token
    serializer_class = AuthTokenSerializer
    # this is the renderer that will be used to render the view
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    # this is the serializer that will be used to generate the token
    serializer_class = UserSerializer
    # this is the authentication class that will be used
    authentication_classes = (authentication.TokenAuthentication,)
    # this is the permission class that will be used
    permission_classes = (permissions.IsAuthenticated,)

    # this is the function that will retrieve the user that is authenticated
    def get_object(self):
        """Retrieve and return authenticated user."""
        # the user is going to be attached to the request
        return self.request.user
