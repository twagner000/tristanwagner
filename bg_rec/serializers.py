from rest_framework import serializers
from . import models

class BriefBoardGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BoardGame
        fields = ('objectid', 'name')
