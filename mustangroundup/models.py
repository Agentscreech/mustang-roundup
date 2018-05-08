from django.db import models

# Create your models here.

class Car(models.Model):
    owner_name = models.CharField(max_length=200)
    car = models.CharField(max_length=200)
    entry_number = models.IntegerField(default=0, unique=True)


    def __str__(self):
        return self.owner_name + "'s " + self.car

class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name


class Division(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Poll(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)

    class Meta:
        ordering = ('votes',)

    def __str__(self):

        return self.division.name + " " + self.category.name + " " + self.car.owner_name + "'s " + self.car.car

class Show_public(models.Model):
    show = models.BooleanField(default=False)

    def __str__(self):
        return str(self.show)