"""
importing user model and serializer model
"""
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    User Validation
    """
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    def validate_password(self, value):
        """
        validate length of the password
        """
        # pylint: disable=no-self-use
        if len(value) < 4:
            raise serializers.ValidationError("Short Password!")
        return value

    def validate_confirm_password(self, value):
        """
        validate length of confirm password
        """
        # pylint: disable=no-self-use
        if len(value) < 4:
            raise serializers.ValidationError("Short Password!")
        else:
            return value

    def validate(self, data):
        """
        validate for same password
        """
        if data['confirm_password'] != data['password']:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        """
        create user
        """
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        """
        user model
        """
        model = User
        fields = ('id', 'username', 'email', 'password', 'confirm_password')
