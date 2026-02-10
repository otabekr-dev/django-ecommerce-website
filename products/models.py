from django.db import models

class Products(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}|{self.price}'