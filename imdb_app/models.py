from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from user_app.models import Users


class PlatformForStreaming(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 50)
    about = models.CharField(max_length = 200,default = "This is a best streaming platform.")
    website = models.CharField(max_length = 150,blank = True,null = True)

    def __str__(self):
        return self.name
    
class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 100)
    movie_summary = models.CharField(max_length = 250)
    stream_platform = models.ForeignKey(PlatformForStreaming,on_delete = models.CASCADE)
    active = models.BooleanField(default = True)
    avg_rating = models.FloatField(default = 0)
    number_rating = models.IntegerField(default = 0)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title
    
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    review_user = models.ForeignKey(Users,on_delete = models.CASCADE)
    rating = models.PositiveIntegerField(validators = [MinValueValidator(1),MaxValueValidator(5)])
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    review_text = models.TextField(default = None,blank = True)
    active = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add = True)
    update = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"{str(self.rating)} | {self.movie} | {self.review_user}"