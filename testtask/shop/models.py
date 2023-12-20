from django.db import models


class Store(models.Model):
    TYPE_CHOICES = [
        ('SPORT', 'Спорт'),
        ('FOOD', 'Їжа'),
        ('ELECTRONICS', 'Електроніка'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    latitude = models.FloatField()
    longitude = models.FloatField()
    commission = models.FloatField(default=0)


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('WINTER', 'Зима'),
        ('SUMMER', 'Літо'),
        ('FOOTBALL', 'Футбол'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photos = models.FileField(upload_to='products/', null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    keywords = models.TextField(null=True, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name