from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json

# instantiate pusher
pusher = Pusher(
    app_id=config('PUSHER_APP_ID'), 
    key=config('PUSHER_KEY'), 
    secret=config('PUSHER_SECRET'), 
    cluster=config('PUSHER_CLUSTER')
)

@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    items = player.items.all().values()
    players = room.playerNames(player_id)
    return JsonResponse({'uuid': uuid, 'items': list(items), "sprite": player.sprite, "char_class":
        player.char_class,
                         'name':player.user.username, \
                                                 "x_coord":
                                 player.x_coord, "y_coord": player.y_coord,'title':room.title, 'description':room.description, 'curr_room': room.id, 'players':players}, safe=True)


# @csrf_exempt
@api_view(["POST"])
def move(request):
    dirs={"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction']
    room = player.room()
    nextRoomID = None
    if direction == "n":
        nextRoomID = room.n_to
    elif direction == "s":
        nextRoomID = room.s_to
    elif direction == "e":
        nextRoomID = room.e_to
    elif direction == "w":
        nextRoomID = room.w_to
    if nextRoomID is not None and nextRoomID > 0:
        nextRoom = Room.objects.get(id=nextRoomID)
        player.currentRoom=nextRoomID
        player.x_coord = nextRoom.x_coord
        player.y_coord = nextRoom.y_coord
        player.save()
        players = nextRoom.playerNames(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
        for p_uuid in currentPlayerUUIDs:
            pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        for p_uuid in nextPlayerUUIDs:
            pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        return JsonResponse({'name':player.user.username, 'curr_room': nextRoom.id,
                             'title':nextRoom.title,
                             'description':nextRoom.description,
                             'players':players, 'error_msg':"", "x_coord":
                                 player.x_coord, "y_coord": player.y_coord},
                            safe=True)
    else:
        players = room.playerNames(player_id)
        return JsonResponse({'name':player.user.username, "x_coord":
                                 player.x_coord, "y_coord": player.y_coord,
                             'title':room.title, 'description':room.description, 'players':players, 'error_msg':"You cannot move that way."}, safe=True)


@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT - broadcast message to all players in the same room
    player = request.user.player
    data = json.loads(request.body)
    room = player.room()
    currentPlayerUUIDs = room.playerUUIDs(player.uuid)
    for p_uuid in currentPlayerUUIDs:
        pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} says {data["message"]}.'})
    return JsonResponse({'name':player.user.username, 'message': data["message"]}, safe=True)

@api_view(["GET"])
def get_map(request):
    rooms = Room.objects.all().values().order_by('id')
    items = Item.objects.all().values().order_by('id')
    return JsonResponse({"rooms": list(rooms), 'items': list(items)})

@api_view(["POST"])
def grab_item(request):
    player = request.user.player
    data = json.loads(request.body)
    item_id = data['item']
    item = Item.objects.all().filter(id=item_id).values()
    item.player_set.add(player)
    player.items.add(item)
    items = player.items.all().values()
    return JsonResponse({'items': items})


@api_view(["POST"])
def drop_item(request):
    player = request.user.player
    data = json.loads(request.body)
    item_id = data['item']
    item = Item.objects.all().filter(id=item_id).values()
    item.player_set.remove(player)
    player.items.remove(item)
    items = player.items.all().values()
    return JsonResponse({'items': items})

@api_view(["POST"])
def change_char(request):
    player = request.user.player
    data = json.loads(request.body)
    player.sprite = data['sprite']
    player.char_class = data['char_class']
    return JsonResponse({"sprite": player.sprite, "char_class":
        player.char_class})
