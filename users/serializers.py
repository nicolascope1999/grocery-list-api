"""Serializsers for users app."""

from django.contrib.auth import get_user_model, authenticate # authenticate is a helper function that comes with django
# serializer is a way of converting data into a format that can be easily transferred over the network
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _ # this is a convention for converting strings to human readable text


# model serializer is a serializer that is specifically tied to a model in the database
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object."""
    # the model and the additional fields we want to make accessible to the serializer
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True,
                                     'min_length': 5}}

    # override the create function to create a users with an encrypted password
    def create(self, validated_data):
        """Create a new users with encrypted password and return it."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a users, setting the password correctly and return it."""
        # remove the password from the validated data
        password = validated_data.pop('password', None)
        # call the update function on the model
        user = super().update(instance, validated_data)

        # if the password exists then we set the password
        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the users authentication object."""
    # this is the email and password that will be used to authenticate the users
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False # this is to make sure that the password is not trimmed
    )

    # this is the function that validates the data that is passed in
    def validate(self, attrs):
        """Validate and authenticate the users."""
        # attrs is the data that is passed in
        email = attrs.get('email')
        password = attrs.get('password')

        # this is the function that will authenticate the users
        user = authenticate(
            # this is the context that is passed in
            request=self.context.get('request'),
            username=email,
            password=password
        )
        # if the authentication fails then we raise an error
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        # this is the attrs that will be returned
        attrs['users'] = user
        return attrs
