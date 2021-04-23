from django.db import models

# Create your models here.
class testDataPoint(models.Model):
    unique_id = models.CharField(max_length=10, primary_key=True)
    attr1 = models.CharField(max_length=60)
    attr2 = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.attr1


