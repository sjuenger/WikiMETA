# module to evaluate the property dictionary

import json

# global variable for the path to the dictionary
path_to_json_dictionary = "data/property_dictionary.json"


# overload method
#
# recommended == true
# query only those references or qualifiers, that are intended by Wikidata
# .. for References: these are properties, which are a facet of "Wikipedia:Citing sources"
# .. for Qualifiers: these are properties, which are a facet of "restrictive qualifier"
#                                                           ,"non-restrictive qualifier"
#                                                           ,"Wikidata property used as \"depicts\" (P180) qualifier on Commons"
#                                                           ,"Wikidata qualifier"
#
# recommended == false
# query only those references or qualifiers, that are NOT intended by Wikidata
# i.e., who do not fulfil the above mentioned requirements
# BUT are min. 1x times used as a reference / qualifier in Wikidata
#
# recommended == None
# query every property available to the mode

def get_top_x_metadata(x, mode, recommended = None):
    if mode not in ["qualifier", "reference"]:
        error_message = "Not supported mode."
        raise Exception(error_message)

    with open(path_to_json_dictionary, "r") as dict_data:
        property_dictionary = json.load(dict_data)

        result_dictionary = {}

        for PID in property_dictionary:
            # check, if the property is /is not a recommended reference/qualifier by Wikidata
            recommended_bool = True

            if recommended:
                if mode == "reference":
                    recommended_bool = bool(property_dictionary[PID]["is_reference"])
                elif mode == "qualifier":
                    recommended_bool = property_dictionary[PID]["qualifier_class"] != ""
                else:
                    recommended_bool = False
            elif not recommended:
                # --> but they are min. 1x times used as a reference
                if mode == "reference" and int(property_dictionary[PID][mode + "_no"]) > 0:
                    recommended_bool = not bool(property_dictionary[PID]["is_reference"])
                # --> but they are min. 1x times used as a reference
                elif mode == "qualifier" and int(property_dictionary[PID][mode + "_no"]) > 0:
                    recommended_bool = property_dictionary[PID]["qualifier_class"] == ""
                else:
                    recommended_bool = False


            if recommended_bool:
                # check, if the current property is smaller than any property in the result dictionary and swap them
                # or, if the result dictionary has not yet got 'X' entries, just add the property
                if len(result_dictionary) < x:
                    result_dictionary[PID] = property_dictionary[PID]
                else:
                    # no need to check for (non-) recommended properties here (only (non-) recommended properties
                    #   can be added to this dictionary)
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

        # once all the top x entries are created, store them in a .json file
        if recommended == True:
            tmp_string = "_recommended_"
        elif not recommended == True:
            tmp_string = "_non_recommended_"
        else:
            tmp_string = "_"

        with open("data/statistical_information/property_dictionary_top_" + str(x) + tmp_string +
                  mode + "_metadata.json", "w") \
                as result_json:
            json.dump(result_dictionary, result_json)


# query the top facets (properties have) from qualifier / reference
# .. of recommended / non-recommended / overall properties
def get_top_x_facets_from_metadata(x, mode, recommended = None):
    if mode not in ["qualifier", "reference"]:
        error_message = "Not supported mode."
        raise Exception(error_message)

    with open(path_to_json_dictionary, "r") as dict_data:
        property_dictionary = json.load(dict_data)

        facets_dictionary = {}
        # add all available facets as keys to a dictionary
        facets_dictionary["facets"] = get_all_facets_from_property_dictionary()
        # add a counter for the total amount of facets and properties
        facets_dictionary["total_facets"] = 0
        facets_dictionary["total_properties"] = 0


        for PID in property_dictionary:
            # check, if the property is /is not a recommended reference/qualifier by Wikidata
            recommended_bool = True

            if recommended:
                if mode == "reference":
                    recommended_bool = bool(property_dictionary[PID]["is_reference"])
                elif mode == "qualifier":
                    recommended_bool = property_dictionary[PID]["qualifier_class"] != ""
            elif not recommended:
                # --> but they are min. 1x times used as a reference
                if mode == "reference" and int(property_dictionary[PID][mode + "_no"]) > 0:
                    recommended_bool = not bool(property_dictionary[PID]["is_reference"])
                # --> but they are min. 1x times used as a reference
                elif mode == "qualifier" and int(property_dictionary[PID][mode + "_no"]) > 0:
                    recommended_bool = property_dictionary[PID]["qualifier_class"] == ""
                else:
                    recommended_bool = False

            if recommended_bool:
                facets_dictionary["total_properties"] += 1
                current_facet_list = property_dictionary[PID]["facet_of"]

                for facet in current_facet_list:
                    facets_dictionary["total_facets"] += 1
                    facets_dictionary["facets"][facet] += 1

            # extract the top x facets by usages
            result_facets_dictionary = {"facets" : {}}
            result_facets_dictionary["total_facets"] = facets_dictionary["total_facets"]
            result_facets_dictionary["total_properties"] = facets_dictionary["total_properties"]

            for facet in facets_dictionary["facets"]:
                if len(result_facets_dictionary["facets"]) < x:
                    result_facets_dictionary["facets"][facet] = facets_dictionary["facets"][facet]
                else:
                    # swap with the smallest in the result list
                    smallest_ID = ""
                    for facet_ID in result_facets_dictionary["facets"]:
                        if smallest_ID == "" or \
                                int(result_facets_dictionary["facets"][facet_ID]) \
                                < int(result_facets_dictionary["facets"][smallest_ID]):
                            smallest_ID = facet_ID

                    result_facets_dictionary["facets"].pop(smallest_ID)
                    result_facets_dictionary["facets"][facet] = facets_dictionary["facets"][facet]

        # once all the top x entries are creaed, store them in a .json file
        if recommended == True:
            tmp_string = "_recommended_"
        elif recommended == False:
            tmp_string = "_non_recommended_"
        else:
            tmp_string = ""
        with open("data/statistical_information/property_dictionary_top_" + str(x) + tmp_string +
                  mode + "_facets.json", "w") \
                as result_json:
            json.dump(result_facets_dictionary, result_json)


# query only those references or qualifiers, that are intended by Wikidata
# and order them by their facets
def get_top_x_metadata_recommended_by_facet(x, mode):
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
        property_dictionary = json.load(dict_data)

        result_dict = {}

        i = 0
        for PID in property_dictionary:

            tmp_facets_list = property_dictionary[PID]["facet_of"]
            i += 1
            print(i)
            if "Wikipedia:Citing sources" in property_dictionary[PID]["facet_of"]:

                print(PID)
                if PID == "P2093":
                    print(property_dictionary[PID]["facet_of"])

            for facet in tmp_facets_list:

                if facet not in result_dict:
                    result_dict[facet] = 0

        dict_data.close()
        return result_dict
