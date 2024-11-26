import csv, json

from django.http import HttpResponse

from core.views import BaseView, CrudMixin
from field_mgmt.models import Grower, Farm, Field


class FarmList(BaseView, CrudMixin):

	def get(self, request, *args, **kwargs):
		qs = Farm.objects.all()
		qs = qs.select_related('grower')
		results = []
		for obj in qs:
			data = obj.to_data(depth=2)
			results.append(data)
		datastr = json.dumps(results)
		return HttpResponse(datastr)


class Index(BaseView, CrudMixin):

	RECORD_FIELDS = ['pk', 'name', 'area', 'farm__name',
		   'farm__grower__name', 'farm__grower__street_addr',
		   'farm__grower__city', 'farm__grower__state',
		   'farm__grower__zip_code', 'farm__grower__country']

	def get(self, request, *args, **kwargs):
		# get all records according to filters and sorting
		qs = Field.objects.all()
		qs = qs.select_related('farm', 'farm__grower')
		data = list(qs.values(*self.RECORD_FIELDS))
		datastr = json.dumps(data)
		return HttpResponse(datastr)

	def post(self, request, *args, **kwargs):
		# create a new field record
		data = json.loads(request.body)
		del data['pk']
		del data['version']
		newobj = Field(**data)
		self.validate_model_obj(newobj)
		if self.errors:
			return self.http_error(status_code=400)
		newobj.save()
		objdata = newobj.to_data(depth=2)
		datastr = json.dumps(objdata)
		return HttpResponse(datastr)



class FieldRecord(BaseView, CrudMixin):

	#----------------------------------------------------
	def get(self, request, pk, *args, **kwargs):
		# show a single field record
		obj = Field.objects.get(pk=pk)
		data = obj.to_data(depth=2)
		datastr = json.dumps(data)
		return HttpResponse(datastr)

	#----------------------------------------------------
	def put(self, request, pk, *args, **kwargs):
		# update all data in a field record
		obj = Field.objects.get(pk=pk)
		data = json.loads(request.body)
		data['pk'] = pk
		newobj = Field(**data)
		self.validate_model_obj(newobj)
		if self.errors:
			return self.http_error(status_code=400)
		newobj.save()
		objdata = newobj.to_data(depth=2)
		datastr = json.dumps(objdata)
		return HttpResponse(datastr)

	#----------------------------------------------------
	def patch(self, request, pk, *args, **kwargs):
		# update partial data in a field record
		obj = Field.objects.get(pk=pk)
		data = json.loads(request.body)
		for key, val in data.items():
			setattr(obj, key, val)
		self.validate_model_obj(obj)
		if self.errors:
			return self.http_error(status_code=400)
		obj.save()
		objdata = obj.to_data(depth=2)
		datastr = json.dumps(objdata)
		return HttpResponse(datastr)

	#----------------------------------------------------
	def delete(self, request, pk, *args, **kwargs):
		# delete a field record
		obj = Field.objects.get(pk=pk)
		objdata = obj.to_data(depth=2)
		obj.delete()
		datastr = json.dumps(objdata)
		return HttpResponse(datastr)



class ImportData(BaseView, CrudMixin):

	def set_value(self, obj, row, field_name):
		if field_name in row.keys():
			setattr(obj, field_name, row[field_name])

	def get_grower(self, row):
		grower_name = row['grower_name']
		grower = None
		existing_growers = Grower.objects.filter(name=grower_name)
		if len(existing_growers) == 0:
			self.logger.info('No grower with name, creating new grower: {}'.format(grower_name))
			grower = Grower(name=grower_name)
			self.set_value(grower, row, 'street_addr')
			self.set_value(grower, row, 'city')
			self.set_value(grower, row, 'state')
			self.set_value(grower, row, 'zip_code')
			self.set_value(grower, row, 'country')
			if self.validate_model_obj(grower):
				grower.save()
			else:
				grower = None
		elif len(existing_growers) > 1:
			self.log_error('Multiple growers with name: {}'.format(grower_name))
		elif len(existing_growers) == 1:
			grower = existing_growers[0]
		return grower
	
	def get_farm(self, row, grower):
		farm_name = row['farm_name']
		farm = None
		existing_farms = grower.farm_set.filter(name=farm_name)
		if len(existing_farms) == 0:
			self.logger.info('No farm with name, creating new farm: {}'.format(farm_name))
			farm = Farm(name=farm_name, grower=grower)
			if self.validate_model_obj(farm):
				farm.save()
			else:
				farm = None
		elif len(existing_farms) > 1:
			self.log_error('Multiple farms with name: {}'.format(farm_name))
		elif len(existing_farms) == 1:
			farm = existing_farms[0]
		return farm
	
	def get_field(self, row, farm):
		field_name = row['field_name']
		field = None
		existing_fields = farm.field_set.filter(name=field_name)
		if len(existing_fields) == 0:
			self.logger.warning('No field with name, creating new field: {}'.format(field_name))
			area = row['area']
			field = Field(name=field_name, area=area, farm=farm)
			if self.validate_model_obj(field):
				field.save()
			else:
				field = None
		elif len(existing_fields) > 1:
			self.log_error('Multiple field with name: {}'.format(field_name))
		elif len(existing_fields) == 1:
			field = existing_fields[0]
			field.area = row['area']
			if self.validate_model_obj(field):
				field.save()
			else:
				field = None
		return field
	
	def check_required_columns(self, columns):
		passed = True
		if 'grower_name' not in columns:
			passed = False
			self.log_error('No "grower_name" column defined')
		if 'farm_name' not in columns:
			self.log_error('No "farm_name" column defined')
			passed = False
		if 'field_name' not in columns:
			self.log_error('No "field_name" column defined')
			passed = False
		if 'area' not in columns:
			self.log_error('No area column defined')
			passed = False
		return passed
	
	def post(self, request, *args, **kwargs):
		# import CSV data as new field records
		records_read = 0
		records_processed = 0
		columnsValid = None
		success = True
		importdata = request.body.decode('utf-8')
		reader = csv.DictReader(importdata.splitlines())
		if self.check_required_columns(reader.fieldnames):
			for row in reader:
				records_read += 1
				grower = self.get_grower(row)
				if grower is None:
					self.logger.info('GROWER IS NONE')
					continue

				farm = self.get_farm(row, grower)
				if farm is None:
					continue

				field = self.get_field(row, farm)
				if field is not None:
					records_processed += 1

		if self.errors:
			success = False
		data = {
			'records_read': records_read,
			'records_processed': records_processed,
			'status': success,
			'errors': self.errors,
		}
		datastr = json.dumps(data)
		return HttpResponse(datastr)




			


				

