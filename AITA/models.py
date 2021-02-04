from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=500)
    body = models.TextField()
    is_asshole = models.IntegerField()

    class Meta:
       db_table = 'posts'
