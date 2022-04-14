from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import json
from django.http import JsonResponse

from chat.models import Group, User

# Create your views here.
@login_required
def index(request):
    return render(request, "chat/index.html", {
        "groups": request.user.joined_groups.all(),
        "rooms": Group.objects.all()
    })


@login_required
def room(request, group_name):
    try:
        group = Group.objects.get(name=group_name)

    except Group.DoesNotExist:
        return JsonResponse({"error": "Group matching query does not exist."}, status=400)

    return render(request, "chat/room.html", {
        "room_name_json": mark_safe(json.dumps(group.name)),
        "username": mark_safe(json.dumps(request.user.username)),
        "groups": request.user.joined_groups.all(),
        "group": group,
        "rooms": Group.objects.all()
    })


@login_required
def update_room(request, room_id):
    try:
        room = Group.objects.get(pk=room_id)

        if request.user in room.users.all():
            room.users.remove(request.user)
        else:
            room.users.add(request.user)

    except Group.DoesNotExist:
        return JsonResponse({"error": "Group matching query does not exist."}, status=400)

    return JsonResponse({"message": "Updated requested chat room successfully."}, status=201)
    