from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Coders(models.Model):			#OnetoOnefield is used to add more columns to a existing table user in database
	user=models.OneToOneField(User, on_delete=models.CASCADE)
	UserScore=models.IntegerField(default=0)

class Question(models.Model):		#to make questions for coding practice
	user = models.ForeignKey(get_user_model(),on_delete = models.CASCADE,null = True)
	questiontitle = models.CharField(max_length=100)
	question=models.TextField()			#description of question in detail
	difficulty=models.CharField(max_length=10)
	Score=models.IntegerField()
	timestamp = models.DateTimeField(default = timezone.now)

	def __str__(self):
		return self.question

class Answer(models.Model):		#To make answers table 
	question = models.ForeignKey(Question,on_delete = models.CASCADE,related_name = "answers")
	answer = models.TextField()
	timestamp = models.DateTimeField(default = timezone.now)
	user = models.ForeignKey(get_user_model(),on_delete = models.CASCADE, null = True)
	solution=models.TextField()			#Real answer of the output expected 
	#def __str__(self):
		#return self.answer