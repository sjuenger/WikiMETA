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
    with open(path_to_json_dictionary, "r") as dict_data:
        property_dictionary = json.load(dict_data)

        result_dictionary = {}
        result_dictionary["properties"] = {}
        result_dictionary["total_usages_of_" + mode] = 0

        if recommended != None:
            if recommended:
                result_dictionary["total_usages_of_non_reommended_" + mode] = 0
            else:
                result_dictionary["total_usages_of_non_reommended_" + mode] = 0

        result_dictionary["total_unique_properties"] = 0

        for PID in property_dictionary:
            # check, if the property is /is not a recommended reference/qualifier by Wikidata
            recommended_bool = False

            if recommended == True:
                if mode == "reference":
                    recommended_bool = bool(property_dictionary[PID]["is_reference"])
                elif mode == "qualifier":
                    recommended_bool = property_dictionary[PID]["qualifier_class"] != ""
                else:
                    recommended_bool = False

            elif recommended == False:
                # --> but they are min. 1x times used as a reference/qualifier, but not recommended
                if mode == "reference" and int(property_dictionary[PID][mode + "_no"]) > 0\
                        and not bool(property_dictionary[PID]["is_reference"]):
                    recommended_bool = True
                # --> but they are min. 1x times used as a reference/qualifier, but not recommended
                elif mode == "qualifier" and int(property_dictionary[PID][mode + "_no"]) > 0\
                        and property_dictionary[PID]["qualifier_class"] == "":
                    recommended_bool = True
                else:
                    recommended_bool = False

            elif recommended is None:
                # just exclude those, who either aren't a recommended qualifier/reference property
                # .. or are never used as a reference / qualifier
                if (mode == "reference" and (int(property_dictionary[PID][mode + "_no"]) > 0\
                        or bool(property_dictionary[PID]["is_reference"]))):
                    recommended_bool = True
                elif (mode == "qualifier" and (int(property_dictionary[PID][mode + "_no"]) > 0\
                        or property_dictionary[PID]["qualifier_class"] != "")):
                    recommended_bool = True
                else:
                    recommended_bool = False

            if recommended_bool:
                if recommended != None:
                    result_dictionary["total_usages_of_" + recommended + "_" + mode] += \
                        int(property_dictionary[PID][mode + "_no"])
                else:
                    result_dictionary["total_usages_of_" + mode] += \
                        int(property_dictionary[PID][mode + "_no"])
                result_dictionary["total_unique_properties"] += 1
                # check, if the current property is smaller than any property in the result dictionary and swap them
                # or, if the result dictionary has not yet got 'X' entries, just add the property
                if len(result_dictionary["properties"]) < x:
                    result_dictionary["properties"][PID] = property_dictionary[PID]
                else:
                    # no need to check for (non-) recommended properties here (only (non-) recommended properties
                    #   can be added to this dictionary)
                    for result_PID in result_dictionary["properties"]:
                        if PID != result_PID \
                                and (int(property_dictionary[PID][mode + "_no"]) >
                                     int(result_dictionary["properties"][result_PID][mode + "_no"])):

                            # swap with the smallest in the result property
                            smallest_PID = ""
                            for test_PID in result_dictionary["properties"]:
                                if smallest_PID == "" or \
                                        int(result_dictionary["properties"][test_PID][mode + "_no"]) \
                                        < int(result_dictionary["properties"][smallest_PID][mode + "_no"]):
                                    smallest_PID = test_PID

                            result_dictionary["properties"].pop(smallest_PID)
                            result_dictionary["properties"][PID] = property_dictionary[PID]

                            break

            else:
                if recommended != None:
                    result_dictionary["total_usages_of_" + mode] += \
                        int(property_dictionary[PID][mode + "_no"])

        # once all the top x entries are created, store them in a .json file
        if recommended:
            tmp_string = "_recommended_"
        elif recommended is not None:
            tmp_string = "_non_recommended_"
        else:
            tmp_string = "_"

        with open("data/statistical_information/wikidata_research/properties/top_" + str(x) + tmp_string +
                  "for_" + mode + ".json", "w") \
                as result_json:
            json.dump(result_dictionary, result_json)


# query the top facets (properties have) from qualifier / reference
# .. of recommended / non-recommended / overall properties
def get_top_x_facets_by_metadata(x, mode, recommended = None):

    with open(path_to_json_dictionary, "r") as dict_data:
        property_dictionary = json.load(dict_data)

        facets_dictionary = {}
        facets_dictionary["facets"] = {}
        # add a counter for the total amount of facets and properties
        facets_dictionary["total_facets"] = 0
        facets_dictionary["total_properties"] = 0


        for PID in property_dictionary:
            # check, if the property is /is not a recommended reference/qualifier by Wikidata
            recommended_bool = True

            if recommended == True:
                if mode == "reference":
                    recommended_bool = bool(property_dictionary[PID]["is_reference"])
                elif mode == "qualifier":
                    recommended_bool = property_dictionary[PID]["qualifier_class"] != ""
                else:
                    recommended_bool = False

            elif recommended == False:
                # --> but they are min. 1x times used as a reference/qualifier, but not recommended
                if mode == "reference" and int(property_dictionary[PID][mode + "_no"]) > 0\
                        and not bool(property_dictionary[PID]["is_reference"]):
                    recommended_bool = True
                # --> but they are min. 1x times used as a reference/qualifier, but not recommended
                elif mode == "qualifier" and int(property_dictionary[PID][mode + "_no"]) > 0\
                        and property_dictionary[PID]["qualifier_class"] == "":
                    recommended_bool = True
                else:
                    recommended_bool = False

            elif recommended is None:
                # just exclude those, who either aren't a recommended qualifier/reference property
                # .. or are never used as a reference / qualifier
                if mode == "reference" and (int(property_dictionary[PID][mode + "_no"]) > 0\
                        or bool(property_dictionary[PID]["is_reference"])):
                    recommended_bool = True
                elif mode == "qualifier" and (int(property_dictionary[PID][mode + "_no"]) > 0\
                        or property_dictionary[PID]["qualifier_class"] != ""):
                    recommended_bool = True
                else:
                    recommended_bool = False

            if recommended_bool:
                facets_dictionary["total_properties"] += 1
                current_facet_list = property_dictionary[PID]["facet_of"]

                for facet in current_facet_list:
                    facets_dictionary["total_facets"] += 1
                    # add the facet as keys to a dictionary, if it wasn't added before
                    if facet not in facets_dictionary["facets"]:
                        facets_dictionary["facets"][facet] = 1
                    else:
                        facets_dictionary["facets"][facet] += 1

        # extract the top x facets by usages
        result_facets_dictionary = {"facets" : {}}
        result_facets_dictionary["total_facets"] = facets_dictionary["total_facets"]
        result_facets_dictionary["total_properties"] = facets_dictionary["total_properties"]
        result_facets_dictionary["total_unique_facets"] = len(facets_dictionary["facets"])

        for facet in facets_dictionary["facets"]:
            if len(result_facets_dictionary["facets"]) < x:
                result_facets_dictionary["facets"][facet] = facets_dictionary["facets"][facet]
            else:
                # swap with the smallest in the result list -> it is greater than that
                smallest_ID = ""
                for facet_ID in result_facets_dictionary["facets"]:
                    if smallest_ID == "" or \
                            int(result_facets_dictionary["facets"][facet_ID]) \
                            < int(result_facets_dictionary["facets"][smallest_ID]):
                        smallest_ID = facet_ID
                if facets_dictionary["facets"][facet] > facets_dictionary["facets"][smallest_ID]:
                    result_facets_dictionary["facets"].pop(smallest_ID)
                    result_facets_dictionary["facets"][facet] = facets_dictionary["facets"][facet]

        # once all the top x entries are creaed, store them in a .json file
        if recommended:
            tmp_string = "_recommended_"
        elif recommended is not None:
            tmp_string = "_non_recommended_"
        else:
            tmp_string = "_"
        with open("data/statistical_information/wikidata_research/facets/top_" + str(x) + tmp_string +
                  "for_" + mode + ".json", "w") \
                as result_json:
            json.dump(result_facets_dictionary, result_json)


# get the used datatypes for every metadata
# -> a datatype can e.g. be String, WikibaseItem, etc.
#
def get_datatypes_by_metadata(mode, recommended = None):


    with open(path_to_json_dictionary, "r") as dict_data:
        property_dictionary = json.load(dict_data)

        datatypes_dictionary = {}
        datatypes_dictionary["datatypes"] = {}
        # add a counter for the total amount of datatypes and properties
        datatypes_dictionary["total_properties"] = 0


        for PID in property_dictionary:
            # check, if the property is /is not a recommended reference/qualifier by Wikidata
            recommended_bool = True

            if recommended == True:
                if mode == "reference":
                    recommended_bool = bool(property_dictionary[PID]["is_reference"])
                elif mode == "qualifier":
                    recommended_bool = property_dictionary[PID]["qualifier_class"] != ""
                else:
                    recommended_bool = False

            elif recommended == False:
                # --> but they are min. 1x times used as a reference/qualifier, but not recommended
                if mode == "reference" and int(property_dictionary[PID][mode + "_no"]) > 0\
                        and not bool(property_dictionary[PID]["is_reference"]):
                    recommended_bool = True
                # --> but they are min. 1x times used as a reference/qualifier, but not recommended
                elif mode == "qualifier" and int(property_dictionary[PID][mode + "_no"]) > 0\
                        and property_dictionary[PID]["qualifier_class"] == "":
                    recommended_bool = True
                else:
                    recommended_bool = False

            elif recommended is None:
                # just exclude those, who either aren't a recommended qualifier/reference property
                # .. or are never used as a reference / qualifier
                if mode == "reference" and (int(property_dictionary[PID][mode + "_no"]) > 0\
                        or bool(property_dictionary[PID]["is_reference"])):
                    recommended_bool = True
                elif mode == "qualifier" and (int(property_dictionary[PID][mode + "_no"]) > 0\
                        or property_dictionary[PID]["qualifier_class"] != ""):
                    recommended_bool = True
                else:
                    recommended_bool = False

            if recommended_bool:
                datatypes_dictionary["total_properties"] += 1
                current_datatype = property_dictionary[PID]["datatype"]
                # add the datatype as a key to the dictionary, if it wasn't added before
                if current_datatype not in datatypes_dictionary["datatypes"]:
                    datatypes_dictionary["datatypes"][current_datatype] = 1
                else:
                    datatypes_dictionary["datatypes"][current_datatype] += 1

        datatypes_dictionary["total_unique_datatypes"] = len(datatypes_dictionary["datatypes"])


        # once all the top x entries are creaed, store them in a .json file
        if recommended:
            tmp_string = "_recommended_"
        elif recommended is not None:
            tmp_string = "_non_recommended_"
        else:
            tmp_string = "_"

        with open("data/statistical_information/wikidata_research/datatypes/" +
                  "for_" + mode + tmp_string + ".json", "w") \
                as result_json:
            json.dump(datatypes_dictionary, result_json)


# get the accumulated facets by occurences of a (recommended) property in Wikidata
# so, e.g. if "Series Ordinal" occures as a reference 5Miox times in Wikidata, count all of his facets 5Miox times
def get_top_x_facets_by_accumulated_properties(x, mode, recommended = None):

    with open(path_to_json_dictionary, "r") as dict_data:
        property_dictionary = json.load(dict_data)

        facets_dictionary = {}
        facets_dictionary["facets"] = {}
        # add a counter for the total amount of facets and properties
        facets_dictionary["total_accumulated_facets"] = 0
        facets_dictionary["total_accumulated_properties"] = 0

        for PID in property_dictionary:
            # check, if the property is /is not a recommended reference/qualifier by Wikidata
            recommended_bool = True

            if recommended == True:
                if mode == "reference":
                    recommended_bool = bool(property_dictionary[PID]["is_reference"])
                elif mode == "qualifier":
                    recommended_bool = property_dictionary[PID]["qualifier_class"] != ""
                else:
                    recommended_bool = False

            elif recommended == False:
                # --> but they are min. 1x times used as a reference/qualifier, but not recommended
                if mode == "reference" and int(property_dictionary[PID][mode + "_no"]) > 0\
                        and not bool(property_dictionary[PID]["is_reference"]):
                    recommended_bool = True
                # --> but they are min. 1x times used as a reference/qualifier, but not recommended
                elif mode == "qualifier" and int(property_dictionary[PID][mode + "_no"]) > 0\
                        and property_dictionary[PID]["qualifier_class"] == "":
                    recommended_bool = True
                else:
                    recommended_bool = False

            elif recommended is None:
                # just exclude those, who either aren't a recommended qualifier/reference property
                # .. or are never used as a reference / qualifier
                if mode == "reference" and (int(property_dictionary[PID][mode + "_no"]) > 0\
                        or bool(property_dictionary[PID]["is_reference"])):
                    recommended_bool = True
                elif mode == "qualifier" and (int(property_dictionary[PID][mode + "_no"]) > 0\
                        or property_dictionary[PID]["qualifier_class"] != ""):
                    recommended_bool = True
                else:
                    recommended_bool = False

            if recommended_bool:
                facets_dictionary["total_accumulated_properties"] += int(property_dictionary[PID][mode + "_no"])
                current_facet_list = property_dictionary[PID]["facet_of"]
                facets_dictionary["total_accumulated_facets"] += \
                    len(current_facet_list) * int(property_dictionary[PID][mode + "_no"])

                for facet in current_facet_list:
                    # add the facet as keys to a dictionary, if it wasn't added before
                    if facet not in facets_dictionary["facets"]:
                        facets_dictionary["facets"][facet] = int(property_dictionary[PID][mode + "_no"])
                    else:
                        facets_dictionary["facets"][facet] += int(property_dictionary[PID][mode + "_no"])

        # extract the top x facets by usages
        result_facets_dictionary = {"facets": {}}
        result_facets_dictionary["total_accumulated_facets"] = facets_dictionary["total_accumulated_facets"]
        result_facets_dictionary["total_accumulated_properties"] = facets_dictionary["total_accumulated_properties"]

        for facet in facets_dictionary["facets"]:
            if len(result_facets_dictionary["facets"]) < x:
                result_facets_dictionary["facets"][facet] = facets_dictionary["facets"][facet]
            else:
                # swap with the smallest in the result list -> it is greater than that
                smallest_ID = ""
                for facet_ID in result_facets_dictionary["facets"]:
                    if smallest_ID == "" or \
                            int(result_facets_dictionary["facets"][facet_ID]) \
                            < int(result_facets_dictionary["facets"][smallest_ID]):
                        smallest_ID = facet_ID
                if facets_dictionary["facets"][facet] > facets_dictionary["facets"][smallest_ID]:
                    result_facets_dictionary["facets"].pop(smallest_ID)
                    result_facets_dictionary["facets"][facet] = facets_dictionary["facets"][facet]

        # once all the top x entries are creaed, store them in a .json file
        if recommended:
            tmp_string = "_recommended_"
        elif recommended is not None:
            tmp_string = "_non_recommended_"
        else:
            tmp_string = "_"
        with open("data/statistical_information/wikidata_research/accumulated_facets/top_"
                  + str(x) + tmp_string + "for_" + mode + ".json", "w") \
                as result_json:
            json.dump(result_facets_dictionary, result_json)


# get the accumulated datatypes by occurences of a (recommended) property in Wikidata
# so, e.g. if "Series Ordinal" occures as a reference 5Miox times in Wikidata, count his datatype 5Miox times
def get_datatypes_by_accumulated_properties(mode, recommended = None):

    with open(path_to_json_dictionary, "r") as dict_data:
        property_dictionary = json.load(dict_data)

        datatypes_dictionary = {}
        datatypes_dictionary["datatypes"] = {}
        # add a counter for the total amount of datatypes and properties
        datatypes_dictionary["total_properties"] = 0
        datatypes_dictionary["total_accumulated_properties"] = 0


        for PID in property_dictionary:
            # check, if the property is /is not a recommended reference/qualifier by Wikidata
            recommended_bool = True

            if recommended == True:
                if mode == "reference":
                    recommended_bool = bool(property_dictionary[PID]["is_reference"])
                elif mode == "qualifier":
                    recommended_bool = property_dictionary[PID]["qualifier_class"] != ""
                else:
                    recommended_bool = False

            elif recommended == False:
                # --> but they are min. 1x times used as a reference/qualifier, but not recommended
                if mode == "reference" and int(property_dictionary[PID][mode + "_no"]) > 0\
                        and not bool(property_dictionary[PID]["is_reference"]):
                    recommended_bool = True
                # --> but they are min. 1x times used as a reference/qualifier, but not recommended
                elif mode == "qualifier" and int(property_dictionary[PID][mode + "_no"]) > 0\
                        and property_dictionary[PID]["qualifier_class"] == "":
                    recommended_bool = True
                else:
                    recommended_bool = False

            elif recommended is None:
                # just exclude those, who either aren't a recommended qualifier/reference property
                # .. or are never used as a reference / qualifier
                if mode == "reference" and (int(property_dictionary[PID][mode + "_no"]) > 0\
                        or bool(property_dictionary[PID]["is_reference"])):
                    recommended_bool = True
                elif mode == "qualifier" and (int(property_dictionary[PID][mode + "_no"]) > 0\
                        or property_dictionary[PID]["qualifier_class"] != ""):
                    recommended_bool = True
                else:
                    recommended_bool = False

            if recommended_bool:
                datatypes_dictionary["total_properties"] += 1
                datatypes_dictionary["total_accumulated_properties"] += int(property_dictionary[PID][mode + "_no"])
                current_datatype = property_dictionary[PID]["datatype"]
                # add the datatype as a key to the dictionary, if it wasn't added before
                if current_datatype not in datatypes_dictionary["datatypes"]:
                    datatypes_dictionary["datatypes"][current_datatype] = int(property_dictionary[PID][mode + "_no"])
                else:
                    datatypes_dictionary["datatypes"][current_datatype] += int(property_dictionary[PID][mode + "_no"])

        datatypes_dictionary["total_unique_datatypes"] = len(datatypes_dictionary["datatypes"])


        # once all the top x entries are creaed, store them in a .json file
        if recommended:
            tmp_string = "_recommended_"
        elif recommended is not None:
            tmp_string = "_non_recommended_"
        else:
            tmp_string = "_"

        with open("data/statistical_information/wikidata_research/accumulated_datatypes/" +
                  "for_" + mode + tmp_string + ".json", "w") \
                as result_json:
            json.dump(datatypes_dictionary, result_json)


# get the cummulated facets by occurences of a (recommended) property in Wikidata
def get_top_x_metadata_recommended_by_facet(x, mode):
    return


# get all datatypes, that are available inside the property dictionary
def get_all_datatypes_from_property_dictionary():
    with open(path_to_json_dictionary, "r") as dict_data:
        property_dictionary = json.load(dict_data)

        result_dict = {}

        i = 0
        for PID in property_dictionary:

            tmp_datatype = property_dictionary[PID]["datatype"]


            if tmp_datatype not in result_dict:
                result_dict[tmp_datatype] = 0


        dict_data.close()
        return result_dict
