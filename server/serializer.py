from rest_framework import serializers

from server.models import Users, Sound


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'name', 'email', 'gender')


class SoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sound
        fields = ('time_start', 'wave', 'label','user_id_id')
