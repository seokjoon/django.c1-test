from django.db import models

# Create your models here.

class App(models.Model):
	pkg = models.CharField(max_length=200, primary_key=True)
	title = models.CharField(max_length=200)
	date = models.DateField()
	modified = models.DateTimeField()
	installed = models.PositiveIntegerField(default=0)
	provider = models.CharField(max_length=200)
	mail = models.EmailField()

	def __str__(self):
		return self.title