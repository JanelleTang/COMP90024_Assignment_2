from django.contrib.gis.db import models

# Create your models here.
class Region(models.Model):
    STATE_NAMES = [
        ('VIC', 'Victoria'),
        ('NSW', 'New South Wales'),
        ('QLD', 'Queensland'),
        ('SA', 'South Australia'), 
    ]
    class level(models.IntegerChoices):
        extreme_neg = 1
        neg = 2
        neutral = 3
        pos = 4
        extreme_pos = 5

    name = models.CharField(max_length=100)
    state = models.CharField(max_length=3, choices=STATE_NAMES)
    city = models.BooleanField(default=False)
    polygon = models.GeometryField()
    sentiment_value = models.DecimalField(max_digits=3,decimal_places=2)
    sentiment_rank = models.IntegerField(choices=level.choices,default = 3)
    n_tweets = models.IntegerField()
    
    def __str__(self):
        return f"{self.name} in {self.state}"