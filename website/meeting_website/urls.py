from django.urls import path

from . import views

urlpatterns = [
    path('clients/create/', views.RegistrationParticipantView.as_view()),
]
