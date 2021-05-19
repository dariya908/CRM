from django.contrib.auth.models import User
from django.db import models


class Dossier(models.Model):
    full_name = models.CharField(max_length=20)
    date_birth = models.DateField()
    gender = models.CharField(choices=(
        ('M','M'),
        ('F','F')
    ),max_length=2)
    image = models.ImageField(blank=True,null=True)
    user = models.OneToOneField(User,on_delete=models.PROTECT)

    def __str__(self):
        return self.full_name


class Car(models.Model):
    dossier = models.ForeignKey(Dossier,on_delete=models.CASCADE,related_name='cars')
    mark = models.CharField(max_length=20)


class Education(models.Model):
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name='schools')
    school_name = models.CharField(max_length=20)


class Warcraft(models.Model):
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name='war_crfts')
    military_area = models.CharField(max_length=20)
