#  Vue.js Web Application


 ```vue/src/```

## ``` App```



 Main entrypoint component for the Vue3 web application.


 This application has the following global properties available:

* ```$auth```: the Authentication store ( ```useAuthStore```)


#  Components


 ```src/components/```

## ``` InputField.vue```



 Component for ```<input>```HTML tags.



* ```id```: HTML ```id```attribute of the ```<input>```
* ```name```: HTML ```name```attribute of the ```<input>```
* ```type```: HTML ```type```attribute of the ```<input>```
* ```label```: the string to display within the ```<label>```of the ```<input>```
* ```disabled```: a boolean which can disable the ```<input>```when true
* ```v-model```: the data which is used in the ```value```of the ```<input>```


## ``` SelectField.vue```



 Component for ```<select>```HTML tags.



* ```id```: HTML ```id```attribute of the ```<select>```
* ```name```: HTML ```name```attribute of the ```<select>```
* ```label```: the string to display within the ```<label>```of the ```<select>```
* ```disabled```: a boolean which can disable the ```<select>```when true
* ```v-model```: the data which is used in the ```value```of the ```<select>```


**NOTE:**  The ```v-model```expects the data to be a list of objects, each with a ```pk```field which it can use to identify the objects.


#  Router Navigation


 ```src/router/```

##  Router Configuration


 ```src/router/index.js```



* ```/fields```: manage fields page ( ```ManageFields.vue```)
* ```/fields/create```: create new field page ( ```EditFieldRecord.vue```)
* ```/fields/id```: edit/delete field page ( ```EditFieldRecord.vue```)
* ```/fields/import```: import CSV data ( ```ImportRecords.vue```)


#  State Management


 ```src/stores/```

##  Authentication


 ```src/stores/auth.js```

## ``` useAuthStore()```



 State store for user authentication.

**Attributes:**

* ```username```: username of the currently logged in user or ```null```
* ```authenticated```: a boolean indicating if authentication succeeded
* ```loginErrors```: a list of errors when logging in fails
* ```authHeaders```: authentication config needed for API calls


#### ``` async function login(username, password) {```


 Make an API call to authenicate a user. If successful, the store is updated to reflect authentication. If failed, the store populates ```loginErrors```with error messages from the server.

#### ``` async function logout() {```


 Make an API call to log out a user. Resets all authentication data in the store.

#  Views


 ```src/views/```

## ``` EditFieldRecord.vue```



 Page which provides inputs to view, create, edit, and delete field records.



* ```createMode```: a boolean indicating if the form is for creating a new record, or editing/deleting an existing record


## ``` ImportRecords.vue```



 Page which allows a user to import CSV data into the application.

## ``` Login.vue```



 Login page for the web application.

## ``` ManageFields.vue```



 Page which has a list of field records, as well as navigation to create field records and import from CSV.

