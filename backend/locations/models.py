from django.contrib.gis.db import models

# Create your models here.
class LGA(models.Model):
    STATE_NAMES = [
        ('victoria', 'Victoria'),
        ('new south wales', 'New South Wales'),
        ('queensland', 'Queensland'),
        ('south australia', 'South Australia'), 
        ('tasmania', 'Tasmania'),
        ('western australia', 'Western Australia'), 
    ]
    class level(models.IntegerChoices):
        extreme_neg = -3
        neg = -2
        slight_neg = -1
        neutral = 0
        slight_pos = 1
        pos = 2
        extreme_pos = 3

    name = models.CharField(max_length=100,primary_key=True)
    display_name = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20, choices=STATE_NAMES)
    polygon = models.GeometryField(null=True)
    sentiment_value = models.DecimalField(max_digits=20,decimal_places=4,default=0)
    sentiment_rank = models.IntegerField(choices=level.choices,default = 3)
    n_tweets = models.IntegerField(default=0)
    def __str__(self):
        return f"LGA {self.name} in {self.state}"

class City(models.Model):
    STATE_NAMES = [
        ('victoria', 'Victoria'),
        ('new south wales', 'New South Wales'),
        ('queensland', 'Queensland'),
        ('south australia', 'South Australia'), 
        ('tasmania', 'Tasmania'),  
        ('western australia', 'Western Australia'), 
    ]
    class level(models.IntegerChoices):
        extreme_neg = -3
        neg = -2
        slight_neg = -1 
        neutral = 0
        slight_pos = 1
        pos = 2
        extreme_pos = 3

    name = models.CharField(max_length=100,primary_key=True)
    display_name = models.CharField(max_length=100)
    state = models.CharField(max_length=20, choices=STATE_NAMES)
    polygon = models.GeometryField(null=True)
    sentiment_value = models.DecimalField(max_digits=20,decimal_places=4,default=0)
    sentiment_rank = models.IntegerField(choices=level.choices,default = 0)
    n_tweets = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.name} in {self.state}"
