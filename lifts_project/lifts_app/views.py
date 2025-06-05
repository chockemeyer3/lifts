# workouts/views.py
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_date
from .models import LiftEntry
from .serializers import LiftEntrySerializer

class LiftEntryViewSet(viewsets.GenericViewSet,
                       mixins.CreateModelMixin):
    """
    Provides:
      - POST /api/lifts/         → create a new LiftEntry
    Custom action:
      - GET  /api/lifts/latest/  → returns JSON list of recent entries, filtered by lift_type
    """
    queryset = LiftEntry.objects.all()
    serializer_class = LiftEntrySerializer

    @action(detail=False, methods=['get'], url_path='latest')
    def latest(self, request):
        """
        GET parameters:
          - lift: one of 'squat','bench','deadlift','ohp'
          - limit: integer (default = 20)
        Returns: JSON list of {date,estimated_1rm}
        """
        lift = request.query_params.get('lift')
        if lift not in dict(LiftEntry._meta.get_field('lift_type').choices):
            return Response(
                {"detail": "Invalid lift."},
                status=status.HTTP_400_BAD_REQUEST
            )

        limit = int(request.query_params.get('limit', 20))
        # Fetch the most recent `limit` entries for that lift
        qs = (LiftEntry.objects
              .filter(lift_type=lift)
              .order_by('-date')[:limit])
        data = [
            {"date": entry.date.isoformat(),
             "estimated_1rm": entry.estimated_1rm}
            for entry in qs[::-1]  # reverse so oldest is first
        ]
        return Response(data)
