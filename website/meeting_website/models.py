from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.contrib.postgres.fields import ArrayField


class Participant(AbstractUser):

    GENDER = [
        ('MAN', 'Man'),
        ('WOMAN', 'Woman')]

    avatar = models.ImageField('Avatar',
                               upload_to='partcipants_avatars')
    gender = models.CharField('Gender', max_length=5, choices=GENDER)
    age = models.PositiveSmallIntegerField('Age',
                                           validators=[MinValueValidator(18)])
    likes_from_user = ArrayField(models.IntegerField('You liked'),
                                 null=True, blank=True, default=list)
    match = models.ManyToManyField('self',
                                   verbose_name='Match',
                                   related_name='matches',
                                   default=None,
                                   null=True,
                                   blank=True,
                                   )
    lat = models.FloatField('Latitude',
                            max_length=20,
                            null=True,
                            blank=True)
    lon = models.FloatField('Longitude',
                            max_length=20,
                            null=True,
                            blank=True
                            )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'участник'
        verbose_name_plural = 'участники'
