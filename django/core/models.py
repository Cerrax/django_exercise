
from concurrency.fields import AutoIncVersionField
from django.db import models

#-== @h1
# Core Models
#-== /core.models.py
#________________________________________


##########################################
#-== @class
class CoreModel(models.Model):
	#-== Abstract base model which tracks
	# when the object was created and last modified.

	# -== *Model Fields:*
	# @deflist
	# created: datetime that the model was added to the database
	# updated: datetime that the most recent change was made to the object

	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class ConcurrentModel(models.Model):
    version = AutoIncVersionField()

    class Meta:
        abstract = True
