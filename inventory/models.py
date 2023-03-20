from django.db import models
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=10,default="")
    slug = models.SlugField(null=False,unique=True)

    def get_absolute_url(self):
        return reverse('ingredients-list')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name
        return super().save(*args, **kwargs)


#This model defines the relationship between an ingredient and a menu_item

class MenuItem(models.Model):
    name = models.CharField(max_length=200,null=False,blank=False)
    price = models.FloatField()
    slug = models.SlugField(null=False, unique=True,default="")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('menu-item-list')


class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem,on_delete=models.CASCADE,default="")
    ingredient = models.ForeignKey(Ingredient,on_delete=models.CASCADE,default="")
    quantity = models.FloatField()
    slug = models.SlugField(null=False,unique=True,default="")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.ingredient.name
        return super().save(*args, **kwargs)



    def __str__(self):
        return f'{self.menu_item}:{self.ingredient}'

class Purchase(models.Model):
    item = models.CharField(max_length=200)
    datetime = models.DateTimeField()
    price = models.FloatField()


    def __str__(self):
        return self.item


