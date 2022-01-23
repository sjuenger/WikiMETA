# the purpose of this module is, to create a text file, which displays the occurrences of every Wikidata property
# .. in the available data
# for this purpose the 'property_dictionary.json' is used

# mode can either ba "reference" or "qualifier" to describe the usage case as
# .. a qualifier
# ->
# .. a reference
# ->

import glob
import json

def count_property_in(location, data_type):

    if data_type not in ["qualifier_metadata", "reference_metadata"]:
        error_message = "Not supported mode."
        raise Exception(error_message)

    # TODO: check, if the property dictionary already exists
    # if
    # TODO: change to only the files, that do contain a property
    # Retrieve all files, ending with .json
    files_json = glob.glob("data/" + location[:21] + "/" +
                             location[22:] + "/" + data_type + "/*.json")

    # get the path to the folder, where the json file about the gathered statistical information
    # .. is stored
    path_to_stat_information = "data/" + location[:21] + "/" + location[22:] + "/" + \
                        data_type.split('/')[0] + "/statistical_information"

    result_dict = {}
    result_dict["properties"] = {}
    result_dict["unique_properties"] = 0
    result_dict["unique_properties"] = 0

    for query_file in files_json:
        with open(query_file, "r") as query:
            query_json = json.load(query)

            where_part = query_json["where"]

            search_dict_deep_for_multiple_reference_properties(where_part)


    return

def search_dict_deep_for_multiple_reference_properties(current_dict):
    # recursive fun
    search_for = "http://www.wikidata.org/prop/reference/P"
    return
