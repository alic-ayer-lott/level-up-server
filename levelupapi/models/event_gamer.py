from django.db import models


class EventGamer(models.Model):

    gamer = models.ForeignKey("Event_Gamer", on_delete=models.CASCADE)
    event = models.ForeignKey("Event_Gamer", on_delete=models.CASCADE)