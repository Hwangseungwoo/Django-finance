from django.db import models


# Create your models here.
class Question(models.Model):
    age = models.TextField()
    gender = models.TextField()
    goal = models.TextField()
    category = models.TextField()
    type = models.TextField()
    grade = models.TextField()
    
class Answer(models.Model):
    obj_finan = models.TextField()
    type_finan = models.TextField()
    obj_insur = models.TextField()
    goal_insur = models.TextField()
    obj_card = models.TextField()

