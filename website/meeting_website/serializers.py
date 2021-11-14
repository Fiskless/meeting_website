from rest_framework import serializers
from .models import Participant
from . import views
import os


class ParticipantCreateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Participant

        fields = ['id',
                  'avatar',
                  'username',
                  'gender',
                  'age',
                  'first_name',
                  'last_name',
                  'password',
                  'password2',
                  'email',
                  'lat',
                  'lon',
                  ]

    def create(self, *args, **kwargs):

        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError(
                {password: "Пароль не совпадает"})
        participant = Participant.objects.create(
            avatar=self.validated_data['avatar'],
            username=self.validated_data['username'],
            gender=self.validated_data['gender'],
            age=self.validated_data['age'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            lat=self.validated_data['lat'],
            lon=self.validated_data['lon'],
            password=password
        )

        image_path_before_watermark = participant.avatar.path

        participant.avatar = views.watermark_with_transparency(
            participant.avatar.path,
            participant.avatar.url,
            'media/water_mark/wm.png',
        )
        participant.save(update_fields=["avatar"])
        os.remove(image_path_before_watermark)

        return participant


class ParticipantMatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participant

        fields = ['email']
        read_only_fields = ['email']


class ParticipantListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participant

        fields = ['id',
                  'avatar',
                  'username',
                  'gender',
                  'age',
                  'first_name',
                  'last_name',
                  'email',
                  'lat',
                  'lon',
                  ]