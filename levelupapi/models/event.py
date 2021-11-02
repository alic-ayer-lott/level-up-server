from django.db import models


class Event(models.Model):

    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    date = models.CharField(max_length=50)
    time = models.IntegerField()
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    attending = models.ManyToManyField("Gamer", through="EventGamer", related_name="attending_events")

    def __str__(self):
        return self.description
