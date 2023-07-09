from django.urls import path

from . import views

urlpatterns = [
    path("", views.rooms, name='rooms'),
    path('create/', views.create_room, name="createRoom"),
    path('<slug:slug>/', views.enter_room, name="enterRoom"),
    path('<slug:slug>/enter/', views.room, name="room"),
    path('<slug:slug>/delete/', views.delete_room, name="deleteRoom"),
]