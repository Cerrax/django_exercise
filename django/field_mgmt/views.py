
from core.views import BaseView


class Index(BaseView):

	def get(self, request, *args, **kwargs):
		# get all records according to filters and sorting
		pass

	def post(self, request, *args, **kwargs):
		# create a new field record
		pass

	def options(self, request, *args, **kwargs):
		# show what is available for a field record
		pass


class FieldRecord(BaseView):

	#----------------------------------------------------
	def get(self, request, pk, *args, **kwargs):
		# show a single field record
		pass

	#----------------------------------------------------
	def put(self, request, pk, *args, **kwargs):
		# update all data in a field record
		pass

	#----------------------------------------------------
	def patch(self, request, pk, *args, **kwargs):
		# update partial data in a field record
		pass

	#----------------------------------------------------
	def delete(self, request, pk, *args, **kwargs):
		# delete a field record
		pass

	#----------------------------------------------------
	def options(self, request, pk, *args, **kwargs):
		# show what is available for a field record
		pass


class ImportData(BaseView):

	def post(self, request, *args, **kwargs):
		# import CSV data as new field records
		pass
