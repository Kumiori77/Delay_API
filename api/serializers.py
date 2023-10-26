from rest_framework import serializers
from .models import Delay

class DelaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delay
        fields = "__all__"