import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from .models import Participant
from .serializers import ParticipantSerializer
from PIL import Image


def watermark_with_transparency(input_image_path, input_image_url, watermark_image_path):
    base_image = Image.open(input_image_path).convert('RGBA')
    watermark = Image.open(watermark_image_path)
    width, height = base_image.size

    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, (0, 0), watermark)
    transparent.show()
    output_image_path = f"{input_image_path.split('.')[0]}.png"
    output_image_url = (f"{input_image_url.split('.')[0]}.png").split('/media')[1]
    transparent.save(output_image_path)
    return output_image_url


class RegistrationParticipantView(generics.CreateAPIView):

    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [permissions.AllowAny]

    # def perform_create(self, serializer, *args, **kwargs):
    #     print(self.request.FILES)
    #     participant = Participant.objects.get(id=self.request.user.get('id'))
    #     return serializer.save(participant=participant)
    #
    # def post(self, request, *args, **kwargs):
    #     serializer = ParticipantSerializer(data=request.data)
    #     data = {}
    #     if serializer.is_valid():
    #         serializer.save()
    #         data['response'] = True
    #         return Response(data, status=status.HTTP_200_OK)
    #     else:
    #         data = serializer.errors
    #         return Response(data)
