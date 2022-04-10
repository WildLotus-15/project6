from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path("", views.index, name="index"),
    path("room/<str:group_name>/", views.room, name="room"),
    path("rooms/", views.chat_rooms, name="rooms"),
    path("update_room/<int:room_id>/", views.update_room, name="update_room")
]