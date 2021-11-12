from django.db import models
from django.contrib.auth.models import AbstractUser


class Participant(AbstractUser):

    GENDER = [
        ('MAN', 'Man'),
        ('WOMAN', 'Woman')]

    avatar = models.ImageField('Avatar')
    gender = models.CharField(max_length=5, choices=GENDER)
    age = models.PositiveSmallIntegerField('Gender')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'участник'
        verbose_name_plural = 'участники'
