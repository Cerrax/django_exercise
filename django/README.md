#  Django Backend


 ```django/```

#  Core Models


 ```core.models.py```

----------------------------------------

## ``` class CoreModel(models.Model):```



 Abstract base model which tracks when the object was created and last modified.


 **Model Fields:**

* ```created```: datetime that the model was added to the database
* ```updated```: datetime that the most recent change was made to the object


## ``` class ConcurrentModel(models.Model):```



 Abstract model which provides optimistic locking. This allows us to prevent row locking when reading data.


 **Model Fields:**

* ```version```: an integer which increments each time the database record is modified



 If the record is submitted to the database and the ```version```does not match what is stored in the database, the transaction is rejected. This allows us to set the database to do writes without locking any rows during a read, since the only way to update a row is if it has not been changed.

**NOTE:**  This may require the database to be set up to not lock per-table or per-row during reads.


#  Core Views


 ```core.views.py```

----------------------------------------

## ``` class UnauthenticatedView(View):```



 Provides the basic elements that all pages will use. See the Django ```View```documentation for more info: [https:docs.djangoproject.com/en/4.2/topics/class-based-views/https:docs.djangoproject.com/en/4.2/topics/class-based-views/](https:docs.djangoproject.com/en/4.2/topics/class-based-views/)

#### ``` def log_error(self, error_msg, exception=None):```


 Handles settings error messages for both the HTML output and the application logs.

**Parameters:**

* ```error_msg```: the message to display
* ```exception```: the exception which should display a stack trace in the log


#### ``` def http_error(self, status_code=500):```


 Convenience method that sends an HTTP response with a specific error code and includes the list of errors logged on the request.

#### ``` def setup(self, request, *args, **kwargs):```


 Defines the context for the template render and prepares the view for dispatch.

#### ``` def check_perms(self, request, *args, **kwargs):```


 Check permissions of the user. As this is the unauthenticated view, nothing happens here.

#### ``` def initialize(self, request, *args, **kwargs):```


 Do any prep work before the view is dispatched. This is blank and should be overriden as needed.

#### ``` def dispatch(self, request, *args, **kwargs):```


 Dispatches the view with the appropriate HTTP method after checking permissions and initializing.


 The Django ```View```class allows the developer to create methods for each HTTP request method type ( ```GET```, ```POST```, ```PUT```, ```PATCH,``````DELETE```, ```OPTIONS```). Any methods which are not included will respond with an HTTP error 405 (Method Not Allowed).

## ``` class BaseView(LoginRequiredMixin, UnauthenticatedView):```



 Adds login requirement and permission checks to basic page.

**Attributes:**

* ```login_url```: the URL to redirect when an unauthenticed user makes a request


#### ``` def check_perms(self, request, *args, **kwargs):```


 Checks that the ```request.user```has the proper permissions. Raises a ```PermissionDenied```exception if they do not.

## ``` class CrudMixin:```



 A View-class mixin which provides methods to simplify CRUD operations (create, read, update, delete).

#### ``` def serialize(self, obj, format='py', fields=None):```


 Serializes an ```obj```into the provided ```format```with the indicated ```fields```.

**Parameters:**

* ```obj```: the Django model object to serialize
* ```format```: a string constant to detrmine the output format ( ```PYTHON```, ```JSON```, or ```XML```)
* ```fields```: a list of field names to serialize. If ```None```, all model fields will be serialized


#### ``` def deserialize(self, data, format='py', modelclass=None):```


 Deserializes the ```data```from the provided ```format```into the provided ```modelclass```.

**Parameters:**

* ```data```: the data to deserialize
* ```format```: a string constant to detrmine the input format ( ```PYTHON```, ```JSON```, or ```XML```)
* ```modelclass```: when using ```PYTHON```format, the model which the Python data shoudl be populated into



 Using ```JSON```or ```XML```formats will require the ```data```to be formatted according to the standard Django serialization formats. ( [https:docs.djangoproject.com/en/4.2/topics/serialization/https:docs.djangoproject.com/en/4.2/topics/serialization/](https:docs.djangoproject.com/en/4.2/topics/serialization/)) When using ```PYTHON```format, the ```modelclass```must be provided so that the proper model object can be instantiated.

#### ``` def validate(self, modelclass, data):```


 Convenience method that will instantiate the ```data```into the ```modelclass```and then validate it.

#### ``` def validate_model_obj(self, obj):```


 Convenience method that runs the ```obj.full_clean()```validation and logs any errors to both the logs and the HTML template context.

## ``` class LoginView(UnauthenticatedView):```



 Logs in a valid, active user.

#### ``` POST```


 Authenticates and logs in the user.

## ``` class LogoutView(BaseView):```



 Logs out a user and redirects to login.

#### ``` GET```


 Logs out a user.

#  Field Management Models


 ```field_mgmt.models.py```

----------------------------------------

## ``` class Grower(CoreModel, ConcurrentModel):```



 Contains information about a grower, which can have multiple ```Farm```objects associated.


 **Model Fields:**

* ```name```: the name of the grower
* ```street_addr```: street address of the grower
* ```city```: the city the grower is located
* ```state```: the state/province/region/etc. the grower is located
* ```zip_code```: the postal code the grower is located
* ```country```: the country the grower is located


#### ``` def to_data(self, depth=0):```


 Wrangles the model object data into a Python dictionary that can be easily serialized.

**Parameters:**

* ```depth```: how many nested levels down to traverse



 The ```depth```parameter controls how ```ForeignKey```or other relational fields are wrangled. If ```depth == 0``` then these fields will simply provide the primary key of the related object. **Example:** ```'related_object_id': 23``` If ```depth```is greater than zero, the related object will also call its ```to_data```method.

## ``` class Farm(CoreModel, ConcurrentModel):```



 Contains information about a farm, which can have multiple ```Field```objects associated.


 **Model Fields:**

* ```name```: the name of the grower
* ```grower```: the ```Grower```object this belongs to


#### ``` def to_data(self, depth=0):```


 Wrangles the model object data into a Python dictionary that can be easily serialized.

**Parameters:**

* ```depth```: how many nested levels down to traverse



 The ```depth```parameter controls how ```ForeignKey```or other relational fields are wrangled. If ```depth == 0``` then these fields will simply provide the primary key of the related object. **Example:** ```'related_object_id': 23``` If ```depth```is greater than zero, the related object will also call its ```to_data```method.

## ``` class Field(CoreModel, ConcurrentModel):```



 Contains information about a field from a s pecific farm.


 **Model Fields:**

* ```name```: the name of the grower
* ```area```: a float indicating the area in acres of the field
* ```farm```: the ```Farm```object this belongs to


#### ``` def to_data(self, depth=0):```


 Wrangles the model object data into a Python dictionary that can be easily serialized.

**Parameters:**

* ```depth```: how many nested levels down to traverse



 The ```depth```parameter controls how ```ForeignKey```or other relational fields are wrangled. If ```depth == 0``` then these fields will simply provide the primary key of the related object. **Example:** ```'related_object_id': 23``` If ```depth```is greater than zero, the related object will also call its ```to_data```method.

#  Field Management Views


 ```field_mgmt.views.py```

----------------------------------------

## ``` class FarmList(BaseView, CrudMixin):```



 Provides a list of ```Farm```objects.

#### ``` GET```


 Provides a list of all ```Farm```objects in the database.

## ``` class Index(BaseView, CrudMixin):```



 Provides a list of field records, as well as the ability to create a new field record.

#### ``` GET```


 Provides a list of all ```Field```objects in the database.

#### ``` POST```


 Creates a new ```Field```object with the provided JSON data.

## ``` class FieldRecord(BaseView, CrudMixin):```



 Provide information for a single ```Field```object, as well as the ability to create, update and delete the ```Field```object.

#### ``` GET```


 Provides the data of a single ```Field```object.

**Parameters:**

* ```pk```: the primary key of the field, read from the URL


#### ``` PUT```


 Update all fields of a ```Field```object.

**Parameters:**

* ```pk```: the primary key of the field, read from the URL


#### ``` PATCH```


 Update some fields of a ```Field```object.

**Parameters:**

* ```pk```: the primary key of the field, read from the URL


#### ``` DELETE```


 Remove a ```Field```object from the database.

**Parameters:**

* ```pk```: the primary key of the field, read from the URL


## ``` class ImportData(BaseView, CrudMixin):```



 Allows a user to import CSV data into the database. For more information on the format of the CSV data, see this Google Sheet [https:docs.google.com/spreadsheets/d/1MRdKvWF1WWluxKUHb8MpQ6xtPHGZIZfcOE4ndld7ltE/edit?usp=sharinghttps:docs.google.com/spreadsheets/d/1MRdKvWF1WWluxKUHb8MpQ6xtPHGZIZfcOE4ndld7ltE/edit?usp=sharing](https:docs.google.com/spreadsheets/d/1MRdKvWF1WWluxKUHb8MpQ6xtPHGZIZfcOE4ndld7ltE/edit?usp=sharing)


 This import provides quite a bit of flexibility in how data is handled. If a grower name, farm name, or field name is not in the database, it will be created with any relevant data provided. On the other hand, if there is already an object with the same name, it will instead use that existing object.

**NOTE:**  Existing growers and farms cannot have their data updated by this import, however existing field records can be updated with data from this import. If multiple records are found for the grower, farm, or field, then the record is rejected and not stored in the database. Each record is considered individually and only rejected records will not be imported to the database.


#### ``` POST```


 Imports CSV data received in the request body. The response will be JSON data with details and errors about the import.

#### ``` def set_value(self, obj, row, field_name):```


 Checks the ```row```for a ```field_name```and updates the ```obj```if it finds it.

#### ``` def get_grower(self, row):```


 Tries to identify a ```Grower```object which matches the ```grower_name```in the ```row```. If no ```Grower```object is found, it creates a new one, and populates the data from ```row```. If multiple ```Grower```objects have the same name, it rejects the record.

**Returns:**  A ```Grower```object, or if the record is to be rejected, returns ```None```.


#### ``` def get_farm(self, row, grower):```


 Tries to identify a ```Farm```object which matches the ```farm_name```in the ```row```. If no ```Farm```object is found, it creates a new one, and populates the data from ```row```. If multiple ```Farm```objects have the same name, it rejects the record.

**Returns:**  A ```Farm```object, or if the record is to be rejected, returns ```None```.


#### ``` def get_field(self, row, farm):```


 Tries to identify a ```Field```object which matches the ```field_name```in the ```row```. If no ```Field```object is found, it creates a new one, and populates the data from ```row```. If multiple ```Field```objects have the same name, it rejects the record.

**Returns:**  A ```Field```object, or if the record is to be rejected, returns ```None```.


#### ``` def check_required_columns(self, columns):```


 Checks that all column names required for the import are in the ```columns```parameter.

**Returns:**  ```True```if all required names are found, or ```False```if not.


