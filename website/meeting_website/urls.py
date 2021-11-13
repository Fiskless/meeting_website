from django.urls import path

from . import views

urlpatterns = [
    path('clients/create/', views.RegistrationParticipantView.as_view()),
    path('clients/<int:pk>/match/', views.ParticipantMatchView.as_view()),
]
