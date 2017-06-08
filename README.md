wsdot-traffic-agol-update
=========================

The scripts in this repository are used to update items on ArcGIS Online using data from the [WSDOT Traveler Information API].

References [wsdot-traffic-gp] as a git [submodule].

Requirements
------------

* [ArcGIS Pro] 1.4 or higher
* [ArcGIS API for Python]
* Python 3.X (comes with ArcGIS Pro)

Setup
-----

1. Install [ArcGIS Pro]
2. Install [ArcGIS API for Python]
3. Clone this git repository using the `--recursive` option. (If you've already cloned the repository without using this option, run `git submodule update --init --recursive` to get the submodules.)
    ```console
    git clone --recursive https://github.com/WSDOT-GIS/wsdot-traffic-agol-update.git
    ```
4. Create an environment variable called `WSDOT_TRAFFIC_API_CODE` with its value set to a valid [WSDOT Traveler Information API] access code.
5. Create a file called `login-info.json` containing ArcGIS Online login username and password.
    ### Example ###
    ```json
    {
        "username": "JohnQPublic",
        "password": "Y0urP@55w0rd"
    }
    ```

Scripts
-------

### update.py ###

* Creates File Geodatabase of traffic data.
* Logs into ArcGIS Online (AGOL)
* Uploads zipped GDB to AGOL.
* Publishes the uploaded GDB as a feature service
* Inspired by the [Transportation 511] [overwrite-hosted-features] script



[ArcGIS]:http://resources.arcgis.com/
[ArcGIS API for Python]:https://developers.arcgis.com/python/
[ArcGIS Pro]:http://pro.arcgis.com
[overwrite-hosted-features]:https://github.com/Esri/overwrite-hosted-features
[submodule]:https://git-scm.com/book/en/v2/Git-Tools-Submodules
[Transportation 511]:http://links.esri.com/stategovernment/help/transportation511
[unittest]:https://docs.python.org/3/library/unittest.html
[wsdot-traffic-gp]:https://github.com/WSDOT-GIS/wsdot-traffic-gp/
[WSDOT Traveler Information API]:http://www.wsdot.wa.gov/Traffic/api/
