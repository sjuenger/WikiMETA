import json

# create a list of the extracted properties and combine their facets to them -> using the property_dictionary.json
# .. from the wikidata_research
# .. per timeframe
def create_dict_based_on_properties_dict_timeframe_and_Wikidata_property_dict_per_timeframe(location, mode):
    if mode not in ["qualifier_metadata", "reference_metadata"]:
        error_message = "Not supported mode."
        raise Exception(error_message)

    result_dict = {}
    result_dict["real_wikidata_properties"] = {}
    # in case, someone used a property, e.g. "P969", which is not a property anywhere to be found in Wikidata
    result_dict["false_wikidata_properties"] = {}

    path_to_stat_information = "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" \
                                   + mode + "/properties/properties_counted.json"
    path_to_wikidata_property_dict = "data/property_dictionary.json"

    with open(path_to_stat_information, "r") as stat_info_file:
        stat_info = json.load(stat_info_file)
        with open(path_to_wikidata_property_dict, "r") as wikidata_props_file:
            wikidata_props = json.load(wikidata_props_file)

            for PID in stat_info["properties"]:


                # in case, a property mentioned in a query is in fact not a property to be found on Wikidata
                # NOTE: we can be sure, that the property_dictionary.json of the wikidata_research contains
                # ..  all of the properties, that could have been available at the time the query was prompted,
                # .. because, the data from SQID was extracted in 2022 and the queries are from 2017-2018
                #
                # of cours, someone might just accidentally chose a property PID, that was false in 2017-2018
                # .. but is in fact a property in 2022.
                # But, as far as I see this case, this problem is too hard to solve and will not have any significant
                # .. effect on the results of my analysis
                if(PID not in wikidata_props):
                    result_dict["false_wikidata_properties"][PID] = {}
                    result_dict["false_wikidata_properties"][PID]["occurences"] = stat_info["properties"][PID]
                else:
                    result_dict["real_wikidata_properties"][PID] = {}
                    result_dict["real_wikidata_properties"][PID]["occurences"] = stat_info["properties"][PID]
                    result_dict["real_wikidata_properties"][PID]["facets"] = wikidata_props[PID]["facet_of"]
                    result_dict["real_wikidata_properties"][PID]["datatype"] = wikidata_props[PID]["datatype"]


    path_to_output = "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" \
                                   + mode + "/properties_facets_and_datatypes.json"

    with open(path_to_output, "w") as result_data:
        json.dump(result_dict, result_data)


# get the top x counted facets in the counted properties list for references / qualifiers in the current timeframe
def get_top_x_counted_facets_timeframe(location, x, mode):
    if mode not in ["qualifier_metadata", "reference_metadata"]:
        error_message = "Not supported mode."
        raise Exception(error_message)
    if x < 1:
        error_message = "x must be greater than 0 - can only get the top x elements for x > 0"
        raise Exception(error_message)

    result_dict = {}
    result_dict["facets"] = {}
    result_dict["total_facet"] = 0
    result_dict["unique_facets"] = 0

    facet_dict = {}
    facet_dict["facets"] = {}
    facet_dict["total_facets"] = 0
    facet_dict["unique_facets"] = 0

    path_to_stat_information = "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" \
                                   + mode + "/properties_facets_and_datatypes.json"

    with open(path_to_stat_information, "r") as summarized_data:
        summarized_dict = json.load(summarized_data)

        # create a facet dictionary
        for PID in summarized_dict["real_wikidata_properties"]:
            for facet in summarized_dict["real_wikidata_properties"][PID]["facets"]:

                if (facet not in facet_dict["facets"]):
                    facet_dict["facets"][facet] = 1
                    facet_dict["total_facets"] += 1
                    facet_dict["unique_facets"] += 1
                else:
                    facet_dict["facets"][facet] += 1
                    facet_dict["total_facets"] += 1

        result_dict["unique_facets"] = facet_dict["unique_facets"]
        result_dict["total_facet"] = facet_dict["total_facets"]

        path_to_facet_stat_information = \
            "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" \
            + mode + "/facets/facets.json"

        with open(path_to_facet_stat_information, "w") as result_data:
            json.dump(facet_dict, result_data)

        # get the top x facets in the dictionary
        for facet in facet_dict["facets"]:

            if len(result_dict["facets"]) < x:
                result_dict["facets"][facet] = facet_dict["facets"][facet]
            else:
                # get the smallest element out of the result_dict
                smallest_facet = None
                for test_facet in result_dict["facets"]:
                    if smallest_facet is None:
                        smallest_facet = test_facet
                    elif result_dict["facets"][test_facet] < result_dict["facets"][smallest_facet]:
                        smallest_facet = test_facet

                # if the current element of the facet_dict is greater than the smallest element of the result_dict
                # .. -> swap them in the result_dict
                if result_dict["facets"][smallest_facet] < facet_dict["facets"][facet]:
                    result_dict["facets"].pop(smallest_facet)
                    result_dict["facets"][facet] = facet_dict["facets"][facet]

        summarized_data.close()

    path_to_top_x_stat_information = \
        "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" + mode + "/facets/"\
        + "top_" + str(x) + "_facets.json"

    with open(path_to_top_x_stat_information, "w") as result_data:
        json.dump(result_dict, result_data)


# get the top x counted datytypes in the counted properties list for references / qualifiers in the current timeframe
def get_top_x_counted_datatypes_timeframe(location, x, mode):
    if mode not in ["qualifier_metadata", "reference_metadata"]:
        error_message = "Not supported mode."
        raise Exception(error_message)
    if x < 1:
        error_message = "x must be greater than 0 - can only get the top x elements for x > 0"
        raise Exception(error_message)

    result_dict = {}
    result_dict["datatypes"] = {}
    result_dict["total_datatypes"] = 0
    result_dict["unique_datatypes"] = 0

    datatype_dict = {}
    datatype_dict["datatypes"] = {}
    datatype_dict["total_datatypes"] = 0
    datatype_dict["unique_datatypes"] = 0

    path_to_stat_information = "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" \
                                   + mode + "/properties_facets_and_datatypes.json"

    with open(path_to_stat_information, "r") as summarized_data:
        summarized_dict = json.load(summarized_data)

        # create a datatypes dictionary
        for PID in summarized_dict["real_wikidata_properties"]:
            datatype = summarized_dict["real_wikidata_properties"][PID]["datatype"]

            if (datatype not in datatype_dict["datatypes"]):
                datatype_dict["datatypes"][datatype] = 1
                datatype_dict["total_datatypes"] += 1
                datatype_dict["unique_datatypes"] += 1
            else:
                datatype_dict["datatypes"][datatype] += 1
                datatype_dict["total_datatypes"] += 1

        result_dict["unique_datatypes"] = datatype_dict["unique_datatypes"]
        result_dict["total_datatypes"] = datatype_dict["total_datatypes"]

        path_to_facet_stat_information = \
            "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" \
            + mode + "/datatypes/datatypes.json"

        with open(path_to_facet_stat_information, "w") as result_data:
            json.dump(datatype_dict, result_data)

        # get the top x facets in the dictionary
        for datatype in datatype_dict["datatypes"]:

            if len(result_dict["datatypes"]) < x:
                result_dict["datatypes"][datatype] = datatype_dict["datatypes"][datatype]
            else:
                # get the smallest element out of the result_dict
                smallest_datatype = None
                for test_datatype in result_dict["datatypes"]:
                    if smallest_datatype is None:
                        smallest_datatype = test_datatype
                    elif result_dict["datatypes"][test_datatype] < result_dict["datatypes"][smallest_datatype]:
                        smallest_datatype = test_datatype

                # if the current element of the datatype_dict is greater than the smallest element of the result_dict
                # .. -> swap them in the result_dict
                if result_dict["datatypes"][smallest_datatype] < datatype_dict["datatypes"][datatype]:
                    result_dict["datatypes"].pop(smallest_datatype)
                    result_dict["datatypes"][datatype] = datatype_dict["datatypes"][datatype]

        summarized_data.close()

    path_to_top_x_stat_information = \
        "data/" + location[:21] + "/" + location[22:] + "/statistical_information/"+ mode + \
        "/datatypes/top_" + str(x) + "_datatypes.json"

    with open(path_to_top_x_stat_information, "w") as result_data:
        json.dump(result_dict, result_data)


# get the top x accumulated facets in the counted properties list for references / qualifiers
# .. in the current timeframe
def get_top_x_counted_accumulated_facets_timeframe(location, x, mode):
    if mode not in ["qualifier_metadata", "reference_metadata"]:
        error_message = "Not supported mode."
        raise Exception(error_message)
    if x < 1:
        error_message = "x must be greater than 0 - can only get the top x elements for x > 0"
        raise Exception(error_message)

    result_dict = {}
    result_dict["facets"] = {}
    result_dict["total_accumulated_facet"] = 0
    result_dict["unique_facets"] = 0

    facet_dict = {}
    facet_dict["facets"] = {}
    facet_dict["total_accumulated_facets"] = 0
    facet_dict["unique_facets"] = 0

    path_to_stat_information = "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" \
                                   + mode + "/properties_facets_and_datatypes.json"

    with open(path_to_stat_information, "r") as summarized_data:
        summarized_dict = json.load(summarized_data)

        # create a facet dictionary
        for PID in summarized_dict["real_wikidata_properties"]:
            for facet in summarized_dict["real_wikidata_properties"][PID]["facets"]:

                if (facet not in facet_dict["facets"]):
                    facet_dict["facets"][facet] = \
                        summarized_dict["real_wikidata_properties"][PID]["occurences"]
                    facet_dict["total_accumulated_facets"] += \
                        summarized_dict["real_wikidata_properties"][PID]["occurences"]
                    facet_dict["unique_facets"] += 1
                else:
                    facet_dict["facets"][facet] += \
                        summarized_dict["real_wikidata_properties"][PID]["occurences"]
                    facet_dict["total_accumulated_facets"] += \
                        summarized_dict["real_wikidata_properties"][PID]["occurences"]

        result_dict["unique_facets"] = facet_dict["unique_facets"]
        result_dict["total_accumulated_facet"] = facet_dict["total_accumulated_facets"]

        path_to_facet_stat_information = \
            "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" \
            + mode + "/accumulated_facets/accumulated_facets.json"

        with open(path_to_facet_stat_information, "w") as result_data:
            json.dump(facet_dict, result_data)

        # get the top x facets in the dictionary
        for facet in facet_dict["facets"]:

            if len(result_dict["facets"]) < x:
                result_dict["facets"][facet] = facet_dict["facets"][facet]
            else:
                # get the smallest element out of the result_dict
                smallest_facet = None
                for test_facet in result_dict["facets"]:
                    if smallest_facet is None:
                        smallest_facet = test_facet
                    elif result_dict["facets"][test_facet] < result_dict["facets"][smallest_facet]:
                        smallest_facet = test_facet

                # if the current element of the facet_dict is greater than the smallest element of the result_dict
                # .. -> swap them in the result_dict
                if result_dict["facets"][smallest_facet] < facet_dict["facets"][facet]:
                    result_dict["facets"].pop(smallest_facet)
                    result_dict["facets"][facet] = facet_dict["facets"][facet]

        summarized_data.close()

    path_to_top_x_stat_information = \
        "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" + mode +\
        "/accumulated_facets/top_" + str(x) + "_accumulated_facets.json"

    with open(path_to_top_x_stat_information, "w") as result_data:
        json.dump(result_dict, result_data)


# get the top x accumulated datytypes in the counted properties list for references / qualifiers
# .. in the current timeframe
def get_top_x_counted_accumulated_datatypes_timeframe(location, x, mode):
    if mode not in ["qualifier_metadata", "reference_metadata"]:
        error_message = "Not supported mode."
        raise Exception(error_message)
    if x < 1:
        error_message = "x must be greater than 0 - can only get the top x elements for x > 0"
        raise Exception(error_message)

    result_dict = {}
    result_dict["datatypes"] = {}
    result_dict["total_accumulated_datatypes"] = 0
    result_dict["unique_datatypes"] = 0

    datatype_dict = {}
    datatype_dict["datatypes"] = {}
    datatype_dict["total_accumulated_datatypes"] = 0
    datatype_dict["unique_datatypes"] = 0

    path_to_stat_information = "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" \
                                   + mode + "/properties_facets_and_datatypes.json"

    with open(path_to_stat_information, "r") as summarized_data:
        summarized_dict = json.load(summarized_data)

        # create a datatypes dictionary
        for PID in summarized_dict["real_wikidata_properties"]:
            datatype = summarized_dict["real_wikidata_properties"][PID]["datatype"]

            if (datatype not in datatype_dict["datatypes"]):
                datatype_dict["datatypes"][datatype] = \
                        summarized_dict["real_wikidata_properties"][PID]["occurences"]
                datatype_dict["total_accumulated_datatypes"] += \
                        summarized_dict["real_wikidata_properties"][PID]["occurences"]
                datatype_dict["unique_datatypes"] += 1
            else:
                datatype_dict["datatypes"][datatype] += \
                        summarized_dict["real_wikidata_properties"][PID]["occurences"]
                datatype_dict["total_accumulated_datatypes"] += \
                        summarized_dict["real_wikidata_properties"][PID]["occurences"]

        result_dict["unique_datatypes"] = datatype_dict["unique_datatypes"]
        result_dict["total_accumulated_datatypes"] = datatype_dict["total_accumulated_datatypes"]

        path_to_facet_stat_information = \
            "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" \
            + mode + "/accumulated_datatypes/accumulated_datatypes.json"

        with open(path_to_facet_stat_information, "w") as result_data:
            json.dump(datatype_dict, result_data)

        # get the top x facets in the dictionary
        for datatype in datatype_dict["datatypes"]:

            if len(result_dict["datatypes"]) < x:
                result_dict["datatypes"][datatype] = datatype_dict["datatypes"][datatype]
            else:
                # get the smallest element out of the result_dict
                smallest_datatype = None
                for test_datatype in result_dict["datatypes"]:
                    if smallest_datatype is None:
                        smallest_datatype = test_datatype
                    elif result_dict["datatypes"][test_datatype] < result_dict["datatypes"][smallest_datatype]:
                        smallest_datatype = test_datatype

                # if the current element of the datatype_dict is greater than the smallest element of the result_dict
                # .. -> swap them in the result_dict
                if result_dict["datatypes"][smallest_datatype] < datatype_dict["datatypes"][datatype]:
                    result_dict["datatypes"].pop(smallest_datatype)
                    result_dict["datatypes"][datatype] = datatype_dict["datatypes"][datatype]

        summarized_data.close()

    path_to_top_x_stat_information = \
        "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" + mode + \
        "/accumulated_datatypes/top_" + str(x) + "_accumulated_datatypes.json"

    with open(path_to_top_x_stat_information, "w") as result_data:
        json.dump(result_dict, result_data)