from django.db import models
from django.utils import timezone


class Level(models.Model):
    maturity = models.PositiveSmallIntegerField(null=False)
    date_time = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self) -> str:
        maturity = str(self.maturity)
        return maturity
