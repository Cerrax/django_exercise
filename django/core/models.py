
from concurrency.fields import AutoIncVersionField
from django.db import models

#-== @h1
# Core Models
#-== /core.models.py
#________________________________________


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


#-== @class
class ConcurrentModel(models.Model):
    #-== Abstract model which provides optimistic locking.
	# This allows us to prevent row locking when reading data.

	# -== *Model Fields:*
	# @deflist
	# version: an integer which increments each time the database record is modified
      
	#-== If the record is submitted to the database and the /version
	# does not match what is stored in the database, the transaction is rejected.
    # This allows us to set the database to do writes without locking any rows during a read,
	# since the only way to update a row is if it has not been changed.
    #@note
    # This may require the database to be set up to not lock per-table or per-row during reads.

    version = AutoIncVersionField()

    class Meta:
        abstract = True
