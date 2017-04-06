"""Logs into ArcGIS Online and updates a feature collection.
Requires ArcGIS Pro installation to supply arcpy module
"""

import json
from sys import stderr

from os.path import exists
from arcgis.gis import GIS, Item
from typing import Iterable
from addtopath import creategdb
from arcgisext import export, TokenManager

_GDB_PATH = "TravelerInfo.gdb.zip"
_LOGIN_JSON_PATH = "login-info.json"
GDB_TITLE = "TravelerInfo"
FOLDER = "TravelerInfo"
TAGS = ("WSDOT", "traffic", "traveler", "transportation")


class PublishError(Exception):
    """An exception raised when publishing to AGOL fails.
    """

    def __init__(self, parent_ex: Exception):
        super().__init__(parent_ex.args)
        # match = re.match(
        #     r"Job (?:(?:failed)|(?:cancelled)|(?:timed out)).",
        #     parent_ex.args[0], re.IGNORECASE)


class MultipleResultsError(Exception):
    """Raised when a search is performed and more than one
    result is returned when only a singe result was expected.
    """

    def __init__(self, search_results: Iterable[Item]):
        self.search_results = search_results
        super().__init__(
            "Too many results. Only a single result was expected.")


class ItemAddFailError(Exception):
    """Raised when failing to add an item to the GIS.
    """

    def __init__(self, parent_ex: RuntimeError):
        super().__init__(parent_ex.args)


def main():
    """Main function executed when script is run
    """
    if not exists(_LOGIN_JSON_PATH):
        raise FileNotFoundError(_LOGIN_JSON_PATH)
    else:
        stderr.write("%s\n" % "Creating or updating GDB")
        # Create or update the file geodatabase.
        creategdb.main()

    if not exists(_GDB_PATH):
        raise FileNotFoundError(_GDB_PATH)

    # Read login parameters from JSON file.
    with open(_LOGIN_JSON_PATH) as login_info_file:
        login_info = json.load(login_info_file)

    # Specify the title that this script will either update or create.

    gis = GIS("https://www.arcgis.com", **login_info)

    # Create or get exising file GDB
    traffic_gdb_item = _find_file_gdb(gis)
    if not traffic_gdb_item:
        traffic_gdb_item = _add_new_gdb(gis)

    # Publish GDB to feature service or get exising service.
    feature_service = _find_feature_svc(gis)
    if not feature_service:
        try:
            feature_service = traffic_gdb_item.publish()
        except Exception as ex:
            # ArcGIS API throws a plain Exception, which is not recommended.
            raise PublishError(ex)
    else:
        print("Updating %s by uploading %s..." % (traffic_gdb_item.title,
                                                  _GDB_PATH))
        traffic_gdb_item.update(data=_GDB_PATH)
        feature_service = traffic_gdb_item.publish(overwrite=True)

    # Create or update feature collection
    feature_collection_item = _find_feature_collection(gis)
    root_uri = gis._portal.resturl
    token_manager = TokenManager(
        gis._username, gis._password, "https://wsdot.maps.arcgis.com",
        root_uri=root_uri)
    if not feature_collection_item:
        export_success = export(feature_service.itemid, root_uri,
                                token_manager, overwrite=False)
    else:
        export_success = export(feature_service.itemid, root_uri,
                                token_manager, feature_collection_item.itemid)


ITEM_TYPE_FEATURE_LAYER = "Feature Layer"
ITEM_TYPE_FILE_GDB = "File Geodatabase"
ITEM_TYPE_FEATURE_COLLECTION = "Feature Collection"


def _search(gis: GIS, item_type: str, title: str=GDB_TITLE):
    """Searches for items owned by the currently logged in user.
    """
    search_results = gis.content.search(
        query="%s owner:%s" % (title, gis.properties.user.username),
        item_type=item_type)
    if len(search_results) <= 0:
        return None
    elif len(search_results) == 1:
        return search_results[0]
    else:
        raise MultipleResultsError(search_results)


def _find_file_gdb(gis: GIS):
    return _search(gis, ITEM_TYPE_FILE_GDB)


def _find_feature_svc(gis: GIS):
    return _search(gis, ITEM_TYPE_FEATURE_LAYER)


def _find_feature_collection(gis: GIS):
    return _search(gis, ITEM_TYPE_FEATURE_COLLECTION)


def _add_new_gdb(gis: GIS):
    return _add_item(gis, ITEM_TYPE_FILE_GDB, _GDB_PATH)


def _add_item(
        gis: GIS, item_type: str, data: str, folder: str=FOLDER) -> Item:
    try:
        new_item = gis.content.add({
            "title": GDB_TITLE,
            "type": item_type,
            "tags": ",".join(TAGS),
            "culture": "en-US"
        }, data=data, folder=folder)
    except (RuntimeError, AttributeError) as ex:
        raise ItemAddFailError(ex)
    return new_item


if __name__ == '__main__':
    main()
