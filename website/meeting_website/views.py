from rest_framework import generics
from rest_framework import permissions
from .models import Participant
from .serializers import ParticipantSerializer, ParticipantMatchSerializer
from PIL import Image
from django.core.mail import send_mail


def send_mail_about_match(username, to_mail):
    return send_mail('У вас взаимная симпатия',
                     f'Вы понравились {username}! Почта участника: {to_mail}',
                     None,
                     [to_mail],
                     fail_silently=False)


def watermark_with_transparency(input_image_path, input_image_url, watermark_image_path):
    base_image = Image.open(input_image_path).convert('RGBA')
    watermark = Image.open(watermark_image_path)
    width, height = base_image.size

    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, (0, 0), watermark)
    output_image_path = f"{input_image_path.split('.')[0]}.png"
    output_image_url = (f"{input_image_url.split('.')[0]}.png").split('/media')[1]
    transparent.save(output_image_path)
    return output_image_url


class RegistrationParticipantView(generics.CreateAPIView):

    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [permissions.AllowAny]


class ParticipantMatchView(generics.RetrieveUpdateAPIView):

    serializer_class = ParticipantMatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = Participant.objects.get(id=self.request.user.id)
        possible_match = Participant.objects.get(pk=self.kwargs['pk'])
        user.match.add(possible_match)
        send_mail_about_match(user.first_name, possible_match.email)
        send_mail_about_match(possible_match.first_name, user.email)
        return possible_match

