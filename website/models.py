from django.db import models
import math
#from django.contrib.auth.models import User
#from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class AsmePipe(models.Model):    
    dn = models.FloatField()
    nps = models.FloatField()
    sch = models.FloatField()
    od = models.FloatField()
    wt = models.FloatField()
    mass = models.FloatField()

    def __str__(self):
        return (f'{self.dn} - {self.sch}')

    @property
    def id_calc(self):
        ind = self.od - (2 * self.wt)
        return ind
    
    @property
    def xsa_calc(self):
        xsa = math.pi * (self.od/2)**2
        return xsa

class FlangeRating(models.Model):    
    material = models.CharField(max_length=20)
    flange_rating = models.CharField(max_length=10)
    max_pressure = models.CharField(max_length=200)
    temp_range = models.CharField(max_length=200)

    def __str__(self):
        return (f'{self.material} - {self.flange_rating}')
