
from django.db import models

from core.models import CoreModel, ConcurrentModel


class Grower(CoreModel, ConcurrentModel):

	name = models.CharField(max_length=100, null=False, blank=False)
	street_addr = models.CharField(max_length=100, null=True, blank=True)
	city = models.CharField(max_length=100, null=True, blank=True)
	state = models.CharField(max_length=100, null=True, blank=True)
	zip_code = models.CharField(max_length=100, null=True, blank=True)
	country = models.CharField(max_length=100, null=True, blank=True)

	def to_data(self, depth=0):
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

class Farm(CoreModel, ConcurrentModel):

	name = models.CharField(max_length=100, null=False, blank=False)
	grower = models.ForeignKey(Grower, on_delete=models.CASCADE , null=False)

	def to_data(self, depth=0):
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


class Field(CoreModel, ConcurrentModel):

	name = models.CharField(max_length=100, null=False, blank=False)
	area = models.FloatField(null=True)
	farm = models.ForeignKey(Farm, on_delete=models.CASCADE , null=False)

	def to_data(self, depth=0):
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