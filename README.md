wsdot-traffic-gp
================

The scripts in this repository can be used to consume [WSDOT Traveler Information API] REST endpoints in [ArcGIS]  software.

[![Build Status](https://travis-ci.org/WSDOT-GIS/wsdot-traffic-gp.svg?branch=master)](https://travis-ci.org/WSDOT-GIS/wsdot-traffic-gp)

Setup
-----
Before using `wsdottraffic.gp` you should run the `createtemplates.py` script.  This will create the `Data\Templates.gdb` file geodatabase.

### Default access code ###
You can set a default access code, so you don't need to provide it via function parameter, by setting an environment variable called `WSDOT_TRAFFIC_API_CODE` to the default access code.

Modules
-------
See the modules' [docstrings] for more details on how to use the scripts.

### wsdottraffic ###
This module provides the ability to query the REST endpoints and return the results as a dictionary.

* Note that this script has no ArcGIS dependencies and can be run without any ArcGIS software installed.

#### wsdottraffic.gp ####
Consume the REST endpoints and return the results as a file geodatabase.

#### wsdottraffic.armcalc  ####
Consumes the ArmCalc web service.

Scripts
-------

### creategdb.py ###

* Downloads data from API
* Creates feature class and tables if not already existing
* If tables exist, truncates them
* Inserts the data into feature classes and tables inside of a file geodatabase.
* Zips the file geodatabase (which is a folder w/ `.gdb` extension).

### createtemplates.py ###

Creates a file geodatabase of template feature classes and tables. This script isn't really usually necessary, as the `creategdb.py` script will only create the tables if they don't already exist.

### dumpjson.py ###

Downloads data from API and exports JSON files: one with the data and one with automatically detected field definitions.

### update.py ###

Performs the same tasks as `creategdb.py`, then...

* Logs into ArcGIS Online (AGOL)
* Uploads zipped GDB to AGOL.
* Publishes the uploaded GDB as a feature service

#### Requirements ####

Prior to running this script, you will need to create a file called `login-info.json` containing login username and password for an AGOL account.

##### Example #####
```json
{
    "username": "JohnQPublic",
    "password": "Y0urP@55w0rd"
}
```

### Unit tests (`test_*.py`) ###

These are test scripts for use with the [unittest] Python module.

[ArcGIS]:http://resources.arcgis.com/
[docstrings]:https://en.wikipedia.org/wiki/Docstring#Python
[unittest]:https://docs.python.org/3/library/unittest.html
[WSDOT Traveler Information API]:http://www.wsdot.wa.gov/Traffic/api/