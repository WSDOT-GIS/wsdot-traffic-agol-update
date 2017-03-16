wsdot-traffic-agol-update
=========================

The scripts in this repository are used to update items on ArcGIS Online using data from the [WSDOT Traveler Information API].

References [wsdot-traffic-gp]

Setup
-----
Before using `wsdottraffic.gp` you should run the `createtemplates.py` script.  This will create the `Data\Templates.gdb` file geodatabase.

### Default access code ###
You can set a default access code, so you don't need to provide it via function parameter, by setting an environment variable called `WSDOT_TRAFFIC_API_CODE` to the default access code.

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

### update.py ###

Performs the same tasks as `creategdb.py`, then...

* Logs into ArcGIS Online (AGOL)
* Uploads zipped GDB to AGOL.
* Publishes the uploaded GDB as a feature service
* Inspired by the [Transportation 511](http://links.esri.com/stategovernment/help/transportation511) [overwrite-hosted-features](https://github.com/Esri/overwrite-hosted-features) script

#### Requirements ####

* [ArcGIS Pro] 1.4 or higher
* [ArcGIS API for Python]
* Python 3.X (comes with ArcGIS Pro)
* Prior to running this script, you will need to create a file called `login-info.json` containing login username and password for an AGOL account.

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
[ArcGIS API for Python]:https://developers.arcgis.com/python/
[ArcGIS Pro]:http://pro[.arcgis.co]m
[unittest]:https://docs.python.org/3/library/unittest.html
[wsdot-traffic-gp]:https://github.com/WSDOT-GIS/wsdot-traffic-gp/
[WSDOT Traveler Information API]:http://www.wsdot.wa.gov/Traffic/api/