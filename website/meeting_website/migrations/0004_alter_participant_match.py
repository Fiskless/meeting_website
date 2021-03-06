# Generated by Django 3.2.9 on 2021-11-13 11:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting_website', '0003_auto_20211113_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='match',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='_meeting_website_participant_match_+', to=settings.AUTH_USER_MODEL, verbose_name='Match'),
        ),
    ]
