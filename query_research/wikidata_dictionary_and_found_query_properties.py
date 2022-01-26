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
                                   + mode + "_properties_counted.json"
    path_to_wikidata_property_dict = "data/property_dictionary.json"

    with open(path_to_stat_information, "r") as stat_info_file:
        stat_info = json.load(stat_info_file)
        with open(path_to_wikidata_property_dict, "r") as wikidata_props_file:
            wikidata_props = json.load(wikidata_props_file)

            for PID in stat_info["properties"]:
                result_dict[PID] = {}
                result_dict[PID]["occurences"] = stat_info["properties"][PID]

                # in case, a property mentioned in a query is in fact not a property to be found on Wikidata
                # NOTE: we can be sure, that the property_dictionary.json of the wikidata_research contains
                # ..  all of the properties, that could have been available at the time the query was prompted,
                # .. because, the data from SQID was extracted in 2022 and the queries are from 2017-2018
                #
                # of cours, someone might just accidentally chose a property PID, that was false in 2017-2018
                # .. but is in fact a property in 2022.
                # But, as far as I see this case, this problem is too hard to solve and will not have any significant
                # .. effect on the results of my analysis
                result_dict[PID]["facets"] = wikidata_props[PID]["facet_of"]
                result_dict[PID]["datatype"] = wikidata_props[PID]["datatype"]

    path_to_output = "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" \
                                   + mode + "_properties_facets_and_datatypes.json"

    with open(path_to_output, "w") as result_data:
        json.dump(result_dict, result_data)


# get the top x counted properties in the counted properties list for references / qualifiers in the current timeframe
def get_top_x_counted_facets_timeframe(location, x, mode):
    if mode not in ["qualifier_metadata", "reference_metadata"]:
        error_message = "Not supported mode."
        raise Exception(error_message)
    if x < 1:
        error_message = "x must be greater than 0 - can only get the top x elements for x > 0"
        raise Exception(error_message)

    result_dict = {}

    path_to_stat_information = "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" \
                                   + mode + "_properties_counted.json"

    with open(path_to_stat_information, "r") as raw_data:
        raw_dict = json.load(raw_data)

        for PID in raw_dict["properties"]:

            if len(result_dict) < x:
                result_dict[PID] = raw_dict["properties"][PID]
            else:
                # get the smallest element out of the result_dict
                smallest_ID = None
                for test_PID in result_dict:
                    if smallest_ID is None:
                        smallest_ID = test_PID
                    elif result_dict[test_PID] < result_dict[smallest_ID]:
                        smallest_ID = test_PID

                # if the current element of the raw_dict is greater than the smallest element of the result_dict
                # .. -> swap them in the result_dict
                if result_dict[smallest_ID] < raw_dict["properties"][PID]:
                    result_dict.pop(smallest_ID)
                    result_dict[PID] = raw_dict["properties"][PID]

        raw_data.close()

    path_to_top_x_stat_information = \
        "data/" + location[:21] + "/" + location[22:] + "/statistical_information/"\
        + "top_" + str(x) + "_" + mode + "_properties_counted.json"

    with open(path_to_top_x_stat_information, "w") as result_data:
        json.dump(result_dict, result_data)