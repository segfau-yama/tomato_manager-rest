from django.db import models
from django.utils import timezone


class Crop(models.Model):
    types = (
        ('replica', 'レプリカ'),
        ('test', 'テスト'),
        ('production', '本番'),
    )

    name = models.CharField(max_length=50, null=False)
    type = models.CharField(max_length=20, choices=types, null=False)

    def __str__(self) -> str:
        name = str(self.name)
        return name


class Tomato(models.Model):
    crop = models.ForeignKey(
        Crop, to_field='id', on_delete=models.CASCADE, null=False)
    red = models.PositiveSmallIntegerField(null=False)
    green = models.PositiveSmallIntegerField(null=False)
    blue = models.PositiveSmallIntegerField(null=False)
    date_time = models.DateTimeField(default=timezone.now, null=True)

    class Meta:
        verbose_name_plural = 'tomatoes'

    def __str__(self) -> str:
        crop_name = str(self.crop.name)
        return crop_name


class Judgement(models.Model):
    forecast = models.ForeignKey(
        Crop, to_field='id', on_delete=models.CASCADE, null=False)
    result_corrcoef = models.BooleanField(null=False)
    result_rgb = models.BooleanField(null=False, default=True)
    date_time = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self) -> str:
        forecast_name = str(self.forecast.name)
        return forecast_name
