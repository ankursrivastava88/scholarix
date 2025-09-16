from django.db import models

# Create your models here.
class Scholarship(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    amount = models.IntegerField()
    duration = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    