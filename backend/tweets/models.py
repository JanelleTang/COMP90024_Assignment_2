from django.db import models

class Area(models.Model):
    STATE_NAMES = [
    ('VIC', 'Victoria'),
    ('NSW', 'New South Wales'),
    ('QLD', 'Queensland'),
    ('SA', 'South Australia'),
]
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=3, choices=STATE_NAMES)
    city = models.BooleanField(default=False)
    polygon = models.CharField(max_length=10000)
    sentiment_value = models.DecimalField(max_digits=3,decimal_places=3)
    n_tweets = models.IntegerField()
    
    def __str__(self):
        return f"{self.name} in {self.state}"