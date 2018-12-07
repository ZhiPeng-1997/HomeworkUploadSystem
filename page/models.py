from django.db import models

# Create your models here.
class StuAccount(models.Model):
	stuID = models.CharField(max_length=13,primary_key=True)
	stuName = models.CharField(max_length=10)
	stuPassword = models.CharField(max_length=30)
	
	def __str__(self):
		return self.stuID
		
class Homework(models.Model):
	hwID = models.CharField(max_length=10,primary_key=True)
	hwName = models.CharField(max_length=60)
	hwContent = models.CharField(max_length=360)
	hwStart = models.DateTimeField()
	hwEnd = models.DateTimeField()
	
	def __str__(self):
		return self.hwName
	
class HomeworkUpload(models.Model):
	hwID = models.CharField(max_length=10)
	stuID = models.CharField(max_length=13)
	
class Admin(models.Model):
	stuID = models.CharField(max_length=13,primary_key=True)
	
	def __str__(self):
		return self.stuID
	
class notice(models.Model):
	noticeTitle = models.CharField(max_length=40)
	noticeContent = models.CharField(max_length=360)
	
class StuCheck(models.Model):
	stuID = models.CharField(max_length=13)
	phone = models.CharField(max_length=13)
	
	def __str__(self):
		return self.stuID
		
		
class StuCheck(models.Model):
	stuID = models.CharField(max_length=13)
	phone = models.CharField(max_length=13)
	
	def __str__(self):
		return self.stuID
		
class statistic(models.Model):
	id = models.CharField(max_length=10,primary_key=True)
	title = models.CharField(max_length=30)
	header = models.CharField(max_length=360)
	allow = models.CharField(max_length=360) # null代表无
	end = models.DateTimeField()

	def __str__(self):
		return self.title
		
class talk(models.Model):
	id = models.AutoField(primary_key=True)#自增id
	nickname = models.CharField(max_length=30)#昵称
	content = models.CharField(max_length=200)#内容
	talk_date = models.DateField(auto_now = True)
	talk_time = models.CharField(max_length=10)
	stuID = models.CharField(max_length=13)