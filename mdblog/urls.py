from django.urls import path
from . import views

urlpatterns = [
    path('', views.DiseaseListView.as_view(), name='mdblog'),
    path('<slug:title>/', views.detail, name='disease')
]