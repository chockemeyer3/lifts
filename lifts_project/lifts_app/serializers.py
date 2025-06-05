# workouts/serializers.py
from rest_framework import serializers
from .models import LiftEntry

class LiftEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LiftEntry
        fields = ['id', 'lift_type', 'date', 'weight', 'reps', 'rpe', 'estimated_1rm']
        read_only_fields = ['id', 'estimated_1rm']
