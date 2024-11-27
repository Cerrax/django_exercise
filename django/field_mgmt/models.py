
from django.db import models
from django.core.validators import MinValueValidator

from core.models import CoreModel, ConcurrentModel

#-== @h1
# Field Management Models
#-== /field_mgmt.models.py
#________________________________________

#-== @class
class Grower(CoreModel, ConcurrentModel):
	#-== Contains information about a grower,
	# which can have multiple /Farm objects associated.

	# -== *Model Fields:*
	# @deflist
	# name: the name of the grower
	# street_addr: street address of the grower
	# city: the city the grower is located
	# state: the state/province/region/etc. the grower is located
	# zip_code: the postal code the grower is located
	# country: the country the grower is located

	name = models.CharField(max_length=100, null=False, blank=False)
	street_addr = models.CharField(max_length=100, null=True, blank=True)
	city = models.CharField(max_length=100, null=True, blank=True)
	state = models.CharField(max_length=100, null=True, blank=True)
	zip_code = models.CharField(max_length=100, null=True, blank=True)
	country = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return self.name

	#-== @method
	def to_data(self, depth=0):
		#-== Wrangles the model object data into a Python dictionary that can be easily serialized.

		#-== @params
		# depth: how many nested levels down to traverse

		#-== The /depth parameter controls how /ForeignKey or other relational fields are wrangled.
		# If /-depth == 0-/ then these fields will simply provide the primary key of the related object.
		# *Example:* /-'related_object_id': 23-/
		# If /depth is greater than zero, the related object will also call its /to_data method.

		data = {
			'pk': self.pk,
			'version': self.version,
			'created': str(self.created),
			'updated': str(self.updated),
			'name': self.name,
			'street_addr': self.street_addr,
			'city': self.city,
			'state': self.state,
			'zip_code': self.zip_code,
			'country': self.country,
		}
		return data


#-== @class
class Farm(CoreModel, ConcurrentModel):
	#-== Contains information about a farm,
	# which can have multiple /Field objects associated.

	# -== *Model Fields:*
	# @deflist
	# name: the name of the grower
	# grower: the /Grower object this belongs to

	name = models.CharField(max_length=100, null=False, blank=False)
	grower = models.ForeignKey(Grower, on_delete=models.CASCADE , null=False)

	def __str__(self):
		return self.name

	#-== @method
	def to_data(self, depth=0):
		#-== Wrangles the model object data into a Python dictionary that can be easily serialized.

		#-== @params
		# depth: how many nested levels down to traverse

		#-== The /depth parameter controls how /ForeignKey or other relational fields are wrangled.
		# If /-depth == 0-/ then these fields will simply provide the primary key of the related object.
		# *Example:* /-'related_object_id': 23-/
		# If /depth is greater than zero, the related object will also call its /to_data method.

		data = {
			'pk': self.pk,
			'version': self.version,
			'created': str(self.created),
			'updated': str(self.updated),
			'name': self.name,
			'grower': self.grower_id
		}
		if depth > 0:
			data['grower'] = self.grower.to_data(depth-1)
		return data


#-== @class
class Field(CoreModel, ConcurrentModel):
	#-== Contains information about a field from a s pecific farm.

	# -== *Model Fields:*
	# @deflist
	# name: the name of the grower
	# area: a float indicating the area in acres of the field
	# farm: the /Farm object this belongs to

	name = models.CharField(max_length=100, null=False, blank=False)
	area = models.FloatField(null=False, validators=[MinValueValidator(0.0001, message='Area must be at least 0.0001 acres.')])
	farm = models.ForeignKey(Farm, on_delete=models.CASCADE , null=False)

	def __str__(self):
		return '{} - {}'.format(self.farm.name, self.name)

	#-== @method
	def to_data(self, depth=0):
		#-== Wrangles the model object data into a Python dictionary that can be easily serialized.

		#-== @params
		# depth: how many nested levels down to traverse

		#-== The /depth parameter controls how /ForeignKey or other relational fields are wrangled.
		# If /-depth == 0-/ then these fields will simply provide the primary key of the related object.
		# *Example:* /-'related_object_id': 23-/
		# If /depth is greater than zero, the related object will also call its /to_data method.

		data = {
			'pk': self.pk,
			'version': self.version,
			'created': str(self.created),
			'updated': str(self.updated),
			'name': self.name,
			'area': self.area,
			'farm': self.farm_id,
		}
		if depth > 0:
			data['farm'] = self.farm.to_data(depth-1)
		return data