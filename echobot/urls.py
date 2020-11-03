from django.urls import path
from . import views

urlpatterns = [
    path('echobot/', views.webhook, name='echobot'),
]