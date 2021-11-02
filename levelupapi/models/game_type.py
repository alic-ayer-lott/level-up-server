from django.db import models


class GameType(models.Model):

    label = models.ForeignKey("game_type", on_delete=models.CASCADE)