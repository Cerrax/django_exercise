import json
import logging

from django.views import View
from django.forms.models import model_to_dict
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#-== @h1
# Core Views
#-== /core.views.py
#________________________________________


#-== @class
class UnauthenticatedView(View):
	#-== Provides the basic elements that all pages will use.
	# See the Django /View documentation for more info:
	#						!https://docs.djangoproject.com/en/4.2/topics/class-based-views/

	#-== @method
	def log_error(self, error_msg, exception=None):
		# -== Handles settings error messages for both
		# the HTML output and the application logs.
		# @params
		# error_msg: the message to display
		# exception: the exception which should display a stack trace in the log

		# if the error_msg is a list of error messages,
		# log each message separately
		logerrorstr = error_msg
		if isinstance(error_msg, list):
			logerrorstr = '\n'.join(error_msg)
		# if there was an exception, log the traceback as well
		if exception:
			self.logger.exception(logerrorstr)
		else:
			self.logger.error(logerrorstr)
		# add the error_msg to the 'errors' context member
		if isinstance(error_msg, list):
			self.errors.extend(error_msg)
		else:
			self.errors.append(error_msg)

	#-== @method
	def http_error(self, status_code=500):
		#-== Convenience method that sends an HTTP response with a specific error code
		# and includes the list of errors logged on the request.

		error_str = json.dumps(self.errors)
		return HttpResponse(error_str, status=status_code)

	#-== @method
	def setup(self, request, *args, **kwargs):
		#-== Defines the context for the template render
		# and prepares the view for dispatch.

		super().setup(request, *args, *kwargs)
		self.logger = logging.getLogger('django.arva.{}'.format(self.__class__.__qualname__))
		self.user = request.user
		self.errors = []

	#-== @method
	def check_perms(self, request, *args, **kwargs):
		#-== Check permissions of the user. As this is
		# the unauthenticated view, nothing happens here.

		pass

	#-== @method
	def initialize(self, request, *args, **kwargs):
		#-== Do any prep work before the view is dispatched.
		# This is blank and should be overriden as needed.

		pass

	#-== @method
	def dispatch(self, request, *args, **kwargs):
		#-== Dispatches the view with the appropriate HTTP method
		# after checking permissions and initializing.

		self.check_perms(request, *args, **kwargs)
		self.initialize(request, *args, **kwargs)
		return super().dispatch(request, *args, **kwargs)

	#-== The Django /View class allows the developer
	# to create methods for each HTTP request method type
	# ( /GET , /POST , /PUT , /PATCH, /DELETE , /OPTIONS ).
	# Any methods which are not included will
	# respond with an HTTP error 405 (Method Not Allowed).

	# def get(self, request, *args, **kwargs):
	# 	pass

	# def post(self, request, *args, **kwargs):
	#	pass

	# def put(self, request, *args, **kwargs):
	# 	pass

	# def patch(self, request, *args, **kwargs):
	# 	pass

	# def delete(self, request, *args, **kwargs):
	# 	pass

	# def options(self, request, *args, **kwargs):
	# 	pass


##########################################
#-== @class
class BaseView(LoginRequiredMixin, UnauthenticatedView):
	#-== Adds login requirement and permission checks to basic page.
	# @attributes
	# login_url: the URL to redirect when an unauthenticed user makes a request

	login_url = '/login/'

	# ----------------------------------------------------
	#-== @method
	def check_perms(self, request, *args, **kwargs):
		#-== Checks that the /request.user has the proper permissions.
		# Raises a /PermissionDenied exception if they do not.

		pass


##########################################
#-== @class
class CrudMixin:
	#-== A View-class mixin which provides methods
	# to simplify CRUD operations (create, read, update, delete).

	PYTHON = 'py'
	JSON = 'json'
	XML = 'xml'
	modelclass = None

	# ----------------------------------------------------
	#-== @method
	def serialize(self, obj, format='py', fields=None):
		#-== Serializes an /obj into the provided /format with the indicated /fields .
		# @params
		# obj: the Django model object to serialize
		# format: a string constant to detrmine
		#			the output format ( /PYTHON , /JSON , or /XML )
		# fields: a list of field names to serialize.
		#			If /None , all model fields will be serialized

		if format == self.PYTHON:
			return model_to_dict(obj, fields=fields)
		elif format in [self.JSON, self.XML]:
			return serializers.serialize(format, obj, fields=fields)
		else:
			raise ValueError('Unsupported serialization format: {}'.format(format))

	# ----------------------------------------------------
	#-== @method
	def deserialize(self, data, format='py', modelclass=None):
		#-== Deserializes the /data from the provided /format into the provided /modelclass .
		# @params
		# data: the data to deserialize
		# format: a string constant to detrmine
		#			the input format ( /PYTHON , /JSON , or /XML )
		# modelclass: when using /PYTHON format, the model
		#			which the Python data shoudl be populated into
		#
		# -== Using /JSON or /XML formats will require the /data to be formatted
		# according to the standard Django serialization formats.
		# 	( !https://docs.djangoproject.com/en/4.2/topics/serialization/ )
		# When using /PYTHON format, the /modelclass must be provided
		# so that the proper model object can be instantiated.

		if format == self.PYTHON:
			if modelclass is None:
				raise ValueError('Python format requires the modelclass to be provided')
			obj = modelclass(**data)
			return obj
		elif format in [self.JSON, self.XML]:
			return serializers.deserialize(format, data)
		else:
			raise ValueError('Unsupported deserialization format: {}'.format(format))

	# ----------------------------------------------------
	#-== @method
	def validate(self, modelclass, data):
		#-== Convenience method that will instantiate
		# the /data into the /modelclass and then validate it.

		obj = self.deserialize(data, self.PYTHON, modelclass)
		self.validate_model_obj(obj)

	# ----------------------------------------------------
	#-== @method
	def validate_model_obj(self, obj):
		#-== Convenience method that runs the /obj.full_clean() validation
		# and logs any errors to both the logs and the HTML template context.
		try:
			obj.full_clean()
			return True
		except ValidationError as exc:
			self.logger.exception('Model validation failed')
			if hasattr(exc, 'error_list'):
				self.errors.extend(exc.error_list)
			if hasattr(exc, 'error_dict'):
				for key, val in exc.error_dict.items():
					err_str = key + ':'
					for error in val:
						err_str += ' '+ error.message
					self.errors.append(err_str)
		return False



##########################################
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(UnauthenticatedView):

	def get(self, request, *args, **kwargs):
		return HttpResponse()

	# ----------------------------------------------------
	#-== @method
	# POST
	#-== Authenticates and logs in the user.

	def post(self, request, *args, **kwargs):
		data = json.loads(request.body)
		self.logger.info(data)
		username = data['username']
		password = data['password']
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponse('logged in')
			else:
				self.log_error("Disabled user attempted to log in: '{}'".format(username))
		else:
			self.log_error("Invalid credentials for username '{}'".format(username))
		
		return self.http_error(status_code=401)



##########################################
#-== @class
class LogoutView(BaseView):
	#-== Logs out a user and redirects to login.

	# ----------------------------------------------------
	#-== @method
	# GET
	#-== Logs out a user.

	def get(self, request, *args, **kwargs):
		logout(request)
		return HttpResponse('logged out')