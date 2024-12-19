from django.db import models
from django.contrib.auth.models import User


class Capital(models.Model):
    country = models.CharField(max_length=100)
    capital_city = models.CharField(max_length=100)
    capital_population = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)
    objects = models.Manager()


    def __str__(self):
        return f"{self.capital_city} - {self.country}"

    class Meta:
        ordering = ['country']
