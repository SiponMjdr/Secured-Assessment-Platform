from django.db import models

# Create your models here.
class User(models.Model):
  # userimg=models.ImageField()
  firstname=models.CharField(max_length=100)
  lastname=models.CharField(max_length=100)
  email=models.EmailField(max_length=100,primary_key=True)
  password=models.CharField(max_length=100)
  contact=models.IntegerField()
  active=models.BooleanField(default=False)

class Question(models.Model):
  question = models.CharField(max_length=500)
  opt1 = models.CharField(max_length=500)
  opt2 = models.CharField(max_length=500)
  opt3 = models.CharField(max_length=500,blank=True)
  opt4 = models.CharField(max_length=500,blank=True)
  correct = models.CharField(max_length=500)

class Result(models.Model):
  user=models.ForeignKey(User, on_delete=models.CASCADE)
  totalquestion=models.IntegerField()
  totalgivenans=models.IntegerField()
  score=models.IntegerField()
  complete=models.BooleanField(default=False)