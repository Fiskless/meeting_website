from rest_framework import generics
from rest_framework import permissions
from .models import Participant
from .serializers import ParticipantCreateSerializer, \
    ParticipantMatchSerializer, ParticipantListSerializer
from PIL import Image
from django.core.mail import send_mail
from django_filters import rest_framework as filters
from geopy.distance import great_circle


def get_distance_between_users(latitude_user,
                               longitude_user,
                               latitude_match,
                               stop_longitude_match):
    user = (latitude_user, longitude_user)
    match = (latitude_match, stop_longitude_match)

    return great_circle(user, match).kilometers


def send_mail_about_match(username, match_mail, to_mail):
    return send_mail('У вас взаимная симпатия',
                     f'Вы понравились {username}! Почта участника: {match_mail}',
                     None,
                     [to_mail],
                     fail_silently=False)


def watermark_with_transparency(input_image_path,
                                input_image_url,
                                watermark_image_path='static/water_mark/wm.png'):
    base_image = Image.open(input_image_path).convert('RGBA')
    width, height = base_image.size

    watermark = Image.open(watermark_image_path)
    wpercent = ((width/2) / float(watermark.size[0]))
    hsize = int((float(watermark.size[1]) * float(wpercent)))
    watermark = watermark.resize((int(width/2), hsize), Image.ANTIALIAS)
    watermark.save(watermark_image_path)

    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, (0, 0), watermark)
    output_image_path = f"{input_image_path.split('.')[0]}.png"
    output_image_url = (f"{input_image_url.split('.')[0]}.png").split('/media')[1]
    transparent.save(output_image_path)
    return output_image_url


class RegistrationParticipantView(generics.CreateAPIView):

    queryset = Participant.objects.all()
    serializer_class = ParticipantCreateSerializer
    permission_classes = [permissions.AllowAny]


class ParticipantMatchView(generics.RetrieveUpdateAPIView):

    serializer_class = ParticipantMatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = Participant.objects.get(id=self.request.user.id)
        possible_match = Participant.objects.get(pk=self.kwargs['pk'])
        user.likes_from_user.append(possible_match.id)
        user.save()
        if user.id in possible_match.likes_from_user:
            user.match.add(possible_match)
            user.likes_from_user.remove(possible_match.id)
            user.save()
            send_mail_about_match(user.first_name, user.email,
                                  possible_match.email)
            send_mail_about_match(possible_match.first_name,
                                  possible_match.email, user.email)
            return possible_match


class ParticipantFilter(filters.FilterSet):
    max_distance = filters.CharFilter(method='get_max_distance',
                                      label='Max distance between users(km)')

    def get_max_distance(self, queryset, name, value):
        all_users = Participant.objects.all()
        current_user = all_users.get(id=self.request.user.id)
        participants = all_users.exclude(id=current_user.id)
        participant_ids = []
        for participant in participants:
            distance = get_distance_between_users(
                current_user.lat, current_user.lon,
                participant.lat, participant.lon
            )
            if distance < float(value):
               participant_ids.append(participant.id)
        return participants.filter(id__in=participant_ids)

    class Meta:
        model = Participant
        fields = ['gender', 'first_name', 'last_name', 'max_distance']


class ParticipantListView(generics.ListAPIView):
    serializer_class = ParticipantListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ParticipantFilter

    def get_queryset(self):
        user_id = self.request.user.id
        return Participant.objects.all().exclude(id=user_id)
