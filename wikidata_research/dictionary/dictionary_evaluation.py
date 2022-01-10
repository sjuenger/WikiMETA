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
        property_dictionary = dict_data.read()

        result_dictionary = {}

        for property in property_dictionary:
            # check, if th current property is smaller than any property in the result dictionary and swap them
            # or, if the result dictionary has not yet got 'X' entries, just add the property
            if len(result_dictionary) < x:
                result_dictionary.update(property)
            else:
                for result_property in result_dictionary:
                    if property["PID"] != result_property["PID"]\
                        and (property[mode + "_no"] > result_property[mode + "_no"]):
                        result_dictionary.popitem(result_property["PID"])
                        result_dictionary.update(property)

        # once all the top x entries are creaed, store them in a .json file
        with open("data/statistical_information/property_dictionary_top_" + x + "_" + mode + "_0metadata", "w")\
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
        property_dictionary = dict_data.read()

        result_dictionary = {}

        for property in property_dictionary:
            # check, if the property is a recommended reference/qualifier by Wikidata
            recommended_bool = False

            if mode == "reference":
                recommended_bool = property["is_reference"]
            elif mode == "qualifier":
                recommended_bool = property["qualifier_class"] != ""

            if recommended_bool:
                # check, if th current property is smaller than any property in the result dictionary and swap them
                # or, if the result dictionary has not yet got 'X' entries, just add the property
                if len(result_dictionary) < x:
                    result_dictionary.update(property)
                else:
                    # no need to check for recommended properties here (only recommended properties can be added to
                    # .. this dictionary
                    for result_property in result_dictionary:
                        if property["PID"] != result_property["PID"]\
                            and (property[mode + "_no"] > result_property[mode + "_no"]):
                            result_dictionary.popitem(result_property["PID"])
                            result_dictionary.update(property)

        # once all the top x entries are creaed, store them in a .json file
        with open("data/statistical_information/property_dictionary_top_" + x + "_" + mode + "_0metadata", "w")\
            as result_json:
            json.dump(result_dictionary, result_json)

# query only those references or qualifiers, that are NOT intended by Wikidata
# i.e., who do not fulfil the above mentioned requirements
def get_top_x_metadata_not_recommended(x, mode):
    if mode not in ["qualifier", "reference"]:
        error_message = "Not supported mode."
        raise Exception(error_message)

    with open(path_to_json_dictionary, "r") as dict_data:
        property_dictionary = dict_data.read()

        result_dictionary = {}

        for property in property_dictionary:
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
                        if property["PID"] != result_property["PID"]\
                            and (property[mode + "_no"] > result_property[mode + "_no"]):
                            result_dictionary.popitem(result_property["PID"])
                            result_dictionary.update(property)

        # once all the top x entries are creaed, store them in a .json file
        with open("data/statistical_information/property_dictionary_top_" + x + "_" + mode + "_0metadata", "w")\
            as result_json:
            json.dump(result_dictionary, result_json)