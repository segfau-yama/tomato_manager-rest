from django.urls import path
from . import views

urlpatterns = [
    path('level/', views.LevelView.as_view(), name='level'),
]
