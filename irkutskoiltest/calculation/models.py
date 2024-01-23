
# Create your models here.
from django.db import models


class Well(models.Model):
    title = models.CharField(max_length=100)
    liquid_yield = models.FloatField(blank=False)
    oil_yield = models.FloatField(blank=False)
    oil_produced = models.FloatField(blank=False)
    oil_reserve = models.FloatField(blank=False)
    water_cut = models.FloatField(blank=False)


class WaterCutCatalog(models.Model):
    water_cut_value = models.FloatField(blank=False)
    first_characteristic = models.FloatField(blank=False)
    second_characteristic = models.FloatField(blank=False)


class FallRate(models.Model):
    month = models.PositiveIntegerField(blank=False)
    first_m = models.FloatField(blank=False)
    second_m = models.FloatField(blank=False)