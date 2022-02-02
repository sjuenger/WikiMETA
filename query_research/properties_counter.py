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

def count_property_in(location, mode, DATATYPES, redundant_mode):

    if mode not in ["qualifier_metadata", "reference_metadata"]:
        error_message = "Not supported metadata mode: ", mode
        raise Exception(error_message)

    if redundant_mode not in ["redundant", "non_redundant"]:
        error_message = "Not supported redundancy mode: ", mode
        raise Exception(error_message)

    result_dict = {}
    result_dict["properties"] = {}
    result_dict["unique_properties"] = 0
    result_dict["total_properties"] = 0

    # get the path to the folder, where the json file about the gathered statistical information
    # .. is stored
    path_to_stat_information = "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" + \
                               redundant_mode + "/" + mode

    for data_type in DATATYPES:
        # TODO: check, if the property dictionary already exists
        # if
        # TODO: change to only the files, that do contain a property
        # if redundant_mode == "redundant" -> retrieve all .json files
        # if redundant_mode == "non_redundant" -> retrieve only non-marked files
        #
        # in any case, exclude the '...deletion_information.json' files --> [0-9] at the end
        if redundant_mode == "redundant":
            # Retrieve all files, ending with .json (also those, starting with a 'x')
            files_json = glob.glob("data/" + location[:21] + "/" +
                                   location[22:] + "/" + data_type + "/*[0-9].json")
        else:
            # Retrieve only the non-redundant files, ending with .json (not those, starting with a 'x')
            # .. only those, starting with a digit
            files_json = glob.glob("data/" + location[:21] + "/" +
                                   location[22:] + "/" + data_type + "/[0-9]*[0-9].json")


        for query_file in files_json:
            with open(query_file, "r") as query:
                query_json = json.load(query)

                # just iterate through SELECT queries
                # TODO: What about the DESCRIBE / ... queries?
                # Count them by hand?
                if query_json["queryType"] == 'SELECT':

                    where_part = query_json["where"]

                    if mode == "reference_metadata":
                        search_list_deep_for_multiple_metadata_properties  \
                            (where_part, "http://www.wikidata.org/prop/reference/P", result_dict)
                    else:
                        search_list_deep_for_multiple_metadata_properties  \
                            (where_part, "http://www.wikidata.org/prop/qualifier/P", result_dict)

    with open(path_to_stat_information + "/raw_counted_properties/properties/properties_counted.json", "w") as result_data:
        json.dump(result_dict, result_data)

    return


def search_dict_deep_for_multiple_metadata_properties(current_dict, look_for, found_prop_dict):
    # recursive fun

    for element in current_dict:
        if type(current_dict[element]) == dict:
            # recursion start
            search_dict_deep_for_multiple_metadata_properties(current_dict[element], look_for, found_prop_dict)
        elif type(current_dict[element]) == list:
            # recursion start
            search_list_deep_for_multiple_metadata_properties(current_dict[element], look_for, found_prop_dict)

        # assuming, we have a key to a singly value here
        # end of recursion
        else:
            if look_for in str(current_dict[element]):
                # get the property PID
                # e.g. "http://www.wikidata.org/prop/reference/P31" -> "P31"
                split_property_string = current_dict[element].split("/")

                if len(split_property_string) == 6:
                    PID = split_property_string[len(split_property_string)-1]
                else:
                    raise Exception

                # add the property to the result dictionary, if it wasn't added before
                if PID not in found_prop_dict["properties"]:
                    found_prop_dict["properties"][PID] = 1
                    found_prop_dict["unique_properties"] += 1
                    found_prop_dict["total_properties"] += 1
                else:
                    found_prop_dict["properties"][PID] += 1
                    found_prop_dict["total_properties"] += 1

    return

def search_list_deep_for_multiple_metadata_properties(current_list, look_for, found_prop_dict):
    # recursive fun

    for element in current_list:
        if type(element) == dict:
            # recursion start
            search_dict_deep_for_multiple_metadata_properties(element, look_for, found_prop_dict)
        elif type(element) == list:
            # recursion start
            search_list_deep_for_multiple_metadata_properties(element, look_for, found_prop_dict)

        # assuming, we have a key to a singly value here
        # end of recursion
        else:
            if look_for in str(element):
                # get the property PID
                # e.g. "http://www.wikidata.org/prop/reference/P31" -> "P31"
                split_property_string = element.split("/")

                if len(split_property_string) == 6:
                    PID = split_property_string[len(split_property_string)-1]
                else:
                    raise Exception

                # add the property to the result dictionary, if it wasn't added before
                if PID not in found_prop_dict["properties"]:
                    found_prop_dict["properties"][PID] = 1
                    found_prop_dict["unique_properties"] += 1
                    found_prop_dict["total_properties"] += 1
                else:
                    found_prop_dict["properties"][PID] += 1
                    found_prop_dict["total_properties"] += 1
                print(found_prop_dict)

    return