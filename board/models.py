from django.db import models

class Board(models.Model):
    id= models.CharField(max_length=30, primary_key=True)
    pw = models.IntegerField(default=0)

    def __str__(self):
        return self.id
