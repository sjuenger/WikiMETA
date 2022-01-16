# module to evaluate the property dictionary

import json

# global variable for the path to the dictionary
path_to_json_dictionary = "data/property_dictionary.json"


# the mode can either be "reference", or "qualifier"
def get_top_x_metadata_overall(x, mode):
    if mode not in ["qualifier", "reference"]:
        error_message = "Not supported mode."
        raise Exception(error_message)

    with open(path_to_json_dictionary, "r") as dict_data:
        property_dictionary = json.load(dict_data)

        result_dictionary = {}
        #property_dictionary = {}

        # if the result dictionary has not yet got 'X' entries, just add the first properties of the property_dictionary
        while(len(result_dictionary) < x):

            (tmp_key, tmp_item) = property_dictionary.popitem()
            result_dictionary[tmp_key] = tmp_item


        for PID in property_dictionary:
            # check, if the current property is greater than any property in the result dictionary and swap it
            # .. with the smallest item in the result property
            for result_PID in result_dictionary:
                if PID != result_PID \
                        and (int(property_dictionary[PID][mode + "_no"]) >
                                int(result_dictionary[result_PID][mode + "_no"])):

                    # swap with the smallest in the result property
                    smallest_PID=""
                    for test_PID in result_dictionary:
                        if smallest_PID == "" or \
                            int(result_dictionary[test_PID][mode + "_no"]) \
                            < int(result_dictionary[smallest_PID][mode + "_no"]):
                            smallest_PID = test_PID

                    result_dictionary.pop(smallest_PID)
                    result_dictionary[PID] = property_dictionary[PID]

                    break

        # once all the top x entries are created, store them in a .json file
        result_path = "data/statistical_information/property_dictionary_top_"+ str(x) + "_" + mode + "_metadata.json"
        with open(result_path, "w") \
                as result_json:
            json.dump(result_dictionary, result_json)


# query only those references or qualifiers, that are intended by Wikidata
# .. for References: these are properties, which are a facet of "Wikipedia:Citing sources"
# .. for Qualifiers: these are properties, which are a facet of "restrictive qualifier"
#                                                           ,"non-restrictive qualifier"
#                                                           ,"Wikidata property used as \"depicts\" (P180) qualifier on Commons"
#                                                           ,"Wikidata qualifier"
def get_top_x_metadata_recommended(x, mode):
    if mode not in ["qualifier", "reference"]:
        error_message = "Not supported mode."
        raise Exception(error_message)

    with open(path_to_json_dictionary, "r") as dict_data:
        property_dictionary = json.load(dict_data)

        result_dictionary = {}

        for PID in property_dictionary:
            # check, if the property is a recommended reference/qualifier by Wikidata
            recommended_bool = False

            if mode == "reference":
                recommended_bool = bool(property_dictionary[PID]["is_reference"])
            elif mode == "qualifier":
                recommended_bool = property_dictionary[PID]["qualifier_class"] != ""

            if recommended_bool:
                # check, if th current property is smaller than any property in the result dictionary and swap them
                # or, if the result dictionary has not yet got 'X' entries, just add the property
                if len(result_dictionary) < x:
                    result_dictionary[PID] = property_dictionary[PID]
                else:
                    # no need to check for recommended properties here (only recommended properties can be added to
                    # .. this dictionary
                    for result_PID in result_dictionary:
                        if PID != result_PID \
                                and (int(property_dictionary[PID][mode + "_no"]) >
                                     int(result_dictionary[result_PID][mode + "_no"])):

                            # swap with the smallest in the result property
                            smallest_PID = ""
                            for test_PID in result_dictionary:
                                if smallest_PID == "" or \
                                        int(result_dictionary[test_PID][mode + "_no"]) \
                                        < int(result_dictionary[smallest_PID][mode + "_no"]):
                                    smallest_PID = test_PID

                            result_dictionary.pop(smallest_PID)
                            result_dictionary[PID] = property_dictionary[PID]

                            break

        # once all the top x entries are creaed, store them in a .json file
        with open("data/statistical_information/property_dictionary_top_" + str(x) + "_recommended_" + mode + "_metadata.json", "w") \
                as result_json:
            json.dump(result_dictionary, result_json)


# query only those references or qualifiers, that are NOT intended by Wikidata
# i.e., who do not fulfil the above mentioned requirements
def get_top_x_metadata_not_recommended(x, mode):
    if mode not in ["qualifier", "reference"]:
        error_message = "Not supported mode."
        raise Exception(error_message)

    with open(path_to_json_dictionary, "r") as dict_data:
        property_dictionary = json.load(dict_data)

        result_dictionary = {}

        for PID in property_dictionary:
            # check, if the property is NOT a recommended reference/qualifier by Wikidata
            non_recommended_bool = False

            if mode == "reference":
                non_recommended_bool != property["is_reference"]
            elif mode == "qualifier":
                non_recommended_bool = property["qualifier_class"] == ""

            if non_recommended_bool:
                # check, if th current property is smaller than any property in the result dictionary and swap them
                # or, if the result dictionary has not yet got 'X' entries, just add the property
                if len(result_dictionary) < x:
                    result_dictionary.update(property)
                else:
                    # no need to check for non-recommended properties here (only non-recommended properties can
                    # .. be added to this dictionary
                    for result_property in result_dictionary:
                        if property["PID"] != result_property["PID"] \
                                and (property[mode + "_no"] > result_property[mode + "_no"]):
                            result_dictionary.popitem(result_property["PID"])
                            result_dictionary.update(property)

        # once all the top x entries are creaed, store them in a .json file
        with open("data/statistical_information/property_dictionary_top_" + x + "_" + mode + "_0metadata", "w") \
                as result_json:
            json.dump(result_dictionary, result_json)


# query only those references or qualifiers, that are intended by Wikidata
# and order them by their facets
def get_top_x_metadata_recommended_by_facet(x, mode):
    return


def get_top_x_facets_from_metadata_overall():
    return


def get_top_x_facets_from_metadata_recommended():
    return


def get_top_x_facets_from_metadata_not_recommended():
    return


def get_top_x_overall_metadata_by_each_facet():
    return


def get_top_x_recommended_metadata_by_each_facet():
    return


def get_top_x_non_recommended_metadata_by_each_facet():
    return


# get all facets, that are available inside the property dictionary
def get_all_facets_from_property_dictionary():
    with open(path_to_json_dictionary, "r") as dict_data:
        property_dictionary = dict_data.read()

        result_list = []

        for poperty in property_dictionary:

            tmp_facets_list = property["facet_of"]

            for facet in tmp_facets_list:

                if facet not in result_list:
                    result_list.append(facet)

        dict_data.close()
        return result_list
