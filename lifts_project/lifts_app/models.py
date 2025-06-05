# workouts/models.py
from django.db import models
from django.utils import timezone

LIFT_CHOICES = [
    ('squat', 'Squat'),
    ('bench', 'Bench Press'),
    ('deadlift', 'Deadlift'),
    ('ohp', 'Overhead Press'),
]

class LiftEntry(models.Model):
    lift_type = models.CharField(max_length=10, choices=LIFT_CHOICES)
    date      = models.DateField(default=timezone.now)
    weight    = models.FloatField(help_text="Weight lifted (lbs)")
    reps      = models.PositiveIntegerField()
    rpe       = models.FloatField(help_text="RPE (Rate of Perceived Exertion), typically 1–10")

    # We’ll compute estimated 1 RM on save, using the Epley formula: 1RM = weight * (1 + reps/30)
    estimated_1rm = models.FloatField(editable=False)

    def save(self, *args, **kwargs):
        # Epley: 1RM ≈ weight * (1 + reps/30)
        self.estimated_1rm = round(self.weight * (1 + self.reps / 30), 1)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_lift_type_display()} • {self.date} • {self.weight}×{self.reps} @RPE{self.rpe}"
