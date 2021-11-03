from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from levelupapi.models import Event, Game

class EventView(ViewSet):
    def list(self, request):
        events = Event.objects.all()
        event_type = self.request.query_params.get('type', None)
        if event_type is not None:
            events = events.filter(event_type__id=event_type)
        serializer = EventSerializer(
            events, many=True, context={'request': request})
        return Response(serializer.data)

    
    def retrieve (self, request, pk=None):
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer (event, context={'request': request})
            return Reponse(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    

    def create(self, request):
        game = Game.objects.get(pk=request.data["gameId"])
        organizer = Game.objects.get(pk=request.daa["organizerId"])

        try:
            event = Event.objects.create(
                game=game,
                description=request.data["description"],
                date=request.data["date"],
                time=request.data["time"],
                organizer=organizer,
                attending=request.data["attending"]
            )
            serializer = EventSerializer(event, context={'request': request})
            return Response(serializer.data)
        
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)