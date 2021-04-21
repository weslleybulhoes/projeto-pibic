from django.urls import path, include
from . import views

urlpatterns = [
    path('clima/', views.Clima.as_view(), name="clima"),
    path('', views.index, name="index")
]


