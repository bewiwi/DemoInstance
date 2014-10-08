# Project DemoInstance
DemoInstance provides an interface to deploy instance of your project on an Openstack cloud. With this project your futur client can deploy an isolated instance for a defined time.

## Interface example

## Installation

```
$ git clone ..
$ pip install -r requirement.txt
$ cp config-dist.ini config.ini
$ vim config.ini
```

## Configuration

DemoInstance have a single ini config file : config.ini
In this file you have many section.

### DEFAULT
```
[DEFAULT]
log_level=DEBUG
```
log_level : list of value here https://docs.python.org/2/library/logging.html#logging-levels

### OPENSTACK
```
[OPENSTACK]
user=user
password=password
tenant=project
url=http://srv-openstack:5000/v2.0
region=regionOne
```

| Argument | Optional | Description |
| -------- | -------- | -------- |
| user | No | openstack user |
| password | No | openstack password |
| tenant | No | openstack tenant |
| url | No | openstack keystone api url |
| region | Yes | [OPTIONAL] openstak region |

### HTTP
```
[HTTP]
port=8080
```
Argument|Optional|Description
--------|--------|--------
port |No|interface/api tcp port

### DATABASE
```
[DATABASE]
connection:mysql://root@localhost:3306/demo
```
Argument|Optional|Description
--------|--------|--------
connection |No|SQLAlchemy connection string of database

Only tested with MySQL

### IMAGE
[IMAGE] section is the template of any [IMAGE\_].  
You can define in this section variable shared with all [IMAGE\_]. The [IMAGE] section do not define a runnable image only section with [IMAGE\__ImageName_] format define runnable image

##### config
Argument|Optional|Description
--------|--------|--------
name |No| Name of instance like "My cool app"
desc |No|Little descrition like "This app is so cooooooool"
info |No|info display after the creation like : "Login/Password are\<br />test/test""
time_default |No|Default instance life time in minute
time_max=80 |Yes|Max instance time life (activate time selection for user)
img |Yes|url of picture. Can be in /instance_image or external link
image_id |No| Openstack image id
flavor_id |No|Openstack flavor id
prefix |No|Openstack prefix name 
check_url |No|url to call to check if app is ready (%ip% is a placeholder with instance address)
soft_url |No|url of the app to redirect the user
max_instance |No|max number of instance


#### example
Example with only one instance:

```
[IMAGE]

[IMAGE_MYAPP]
name=MyAPP
desc=My first app
info=Login/Password are<br />test/test
img=/instance_image/example.png
image_id=34e38945-3b17-4960-80f3-05efea732579
flavor_id=1
time_default=20
prefix=myapp_
check_url=http://%ip%/ok
soft_url=http://%ip%/
max_instance=10
```

Example with three instances

```
[IMAGE]
flavor_id=1

[IMAGE_MYAPP1]
name=MyAPP
desc=My first app
...

[IMAGE_MYAPP2]
name=MyNewAPP
desc=My second app
...


[IMAGE_MYAPP3]
name=MyLastAPP
desc=My last app
flavor_id=2
...
```
In this example just [IMAGE_MYAPP3] run with flavor_id=2 and other image run with flavor_id=1 defined in [IMAGE]

## Run
```
python demo.py
```
