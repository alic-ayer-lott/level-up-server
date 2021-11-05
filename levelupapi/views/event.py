from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from levelupapi.models import Event, Game, Gamer
from django.contrib.auth.models import User

from levelupapi.views.game import GameSerializer


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
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    

    def create(self, request):
        organizer=Gamer.objects.get(user=request.auth.user)
        game=Game.objects.get(pk=request.data["gameId"])

        try:
            event = Event.objects.create(
                game=game,
                description=request.data["description"],
                date=request.data["date"],
                time=request.data["time"],
                organizer=organizer,
                # attending=request.data["attending"]
            )
            serializer = EventSerializer(event, context={'request': request})
            return Response(serializer.data)
        
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):

        try:
            event = Event.objects.get(pk=pk)
            event.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def update(self, request, pk=None):

        organizer = Gamer.objects.get(user=request.auth.user)


        event = Event.objects.get(pk=pk)
        event.game=Game.objects.get(pk=request.data["gameId"]),
        event.description=request.data["description"],
        event.date=request.data["date"],
        event.time=request.data["time"],
        event.organizer=organizer,
        # event.attending=request.data["attending"]

        event.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

class EventUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')

class GamerSerializer(serializers.ModelSerializer):
    user = EventUserSerializer()
    class Meta:
        model = Gamer
        fields = ('id', 'user', 'bio')

class EventGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'title', 'maker', 'number_of_players', 'skill_level', 'game_type', 'gamer')

class EventSerializer(serializers.ModelSerializer):
    organizer = GamerSerializer()
    game = EventGameSerializer()
    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date', 'time', 'organizer')
        depth = 1
