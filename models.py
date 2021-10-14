from decimal import Decimal


from django.db import models
from django.utils import timezone

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class LastUpdateTry(TimeStampedModel):
    data_updated = models.BooleanField(default=False)

class CityModel(models.Model):
    class Meta:
        verbose_name = 'Stadt'
        verbose_name_plural = 'Städte'
    name = models.CharField(max_length=255)
    population = models.DecimalField(default=0, max_digits=30, decimal_places=0)
    population_is_manual_updated = models.BooleanField(default=False)
    def __str__(self):
        return self.name


class RLPCovidDataModel(models.Model):
    class Meta:
        verbose_name = 'Daten: RLP'
        verbose_name_plural = 'Daten: RLP'

    landkreis = models.ForeignKey(CityModel, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    gesamt = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    differenz_vortag = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    hospitalisiert = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    verstorben = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    genesen = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    aktuelle_faelle = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    inzidenz = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    def __str__(self):
        name = self.landkreis.name + " " + str(self.date)
        return name



