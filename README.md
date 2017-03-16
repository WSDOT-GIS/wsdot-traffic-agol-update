wsdot-traffic-agol-update
=========================

The scripts in this repository are used to update items on ArcGIS Online using data from the [WSDOT Traveler Information API].

References [wsdot-traffic-gp]

### Default access code ###
You can set a default access code, so you don't need to provide it via function parameter, by setting an environment variable called `WSDOT_TRAFFIC_API_CODE` to the default access code.

Scripts
-------

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

[ArcGIS]:http://resources.arcgis.com/
[ArcGIS API for Python]:https://developers.arcgis.com/python/
[ArcGIS Pro]:http://pro[.arcgis.co]m
[unittest]:https://docs.python.org/3/library/unittest.html
[wsdot-traffic-gp]:https://github.com/WSDOT-GIS/wsdot-traffic-gp/
[WSDOT Traveler Information API]:http://www.wsdot.wa.gov/Traffic/api/
