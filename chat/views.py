from django.shortcuts import render, redirect, get_object_or_404
from chat.models import Room, Message
from django.http import JsonResponse
from django.http import HttpResponse, Http404
# Create your views here.
def home(request):
    return render(request, 'home.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username':username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)
    

def send(request):
    if request.method == "POST":
        message = request.POST.get('message')
        username = request.POST.get('username')
        room_id = request.POST.get('room_id')

        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return HttpResponse("Room not found", status=404)

        new_message = Message.objects.create(value=message, user=username, room=room)
        new_message.save()

        return HttpResponse('Message sent successfully')
    else:
        return HttpResponse("Invalid request method", status=405)

def getMessages(request, room):
    try:
        room_details = Room.objects.get(name=room)
    except Room.DoesNotExist:
        return JsonResponse({"error": "Room not found"}, status=404)

    messages = Message.objects.filter(room=room_details)
    return JsonResponse({"messages": list(messages.values())})