import glob
import json


# the purpose of this module is to summarize the many different statistical information at different stages
# .. in the /data folder to one for every 'hierarchy step'
# e.g. -> summarize the information in the different timeframes to the overall ones

# summarize the statistical information about the different "sub-metadata" e.g. 'derived_+_reference_property'
# .. to one .json file for the entire metadata
# .. e.g. for References, Qualifiers, Ranks
def summarize_statistical_information_about_scenarios(location, datatype_list, metadata, redundant_mode):
    # struct for the resulting .json object

    if metadata not in ["qualifier_metadata", "reference_metadata", "rank_metadata"]:
        error_message = "Not supported metadata mode: ", metadata
        raise Exception(error_message)

    if redundant_mode not in ["redundant", "non_redundant"]:
        error_message = "Not supported redundancy mode: ", redundant_mode
        raise Exception(error_message)

    dict_looking_for = {
        "looking_for": metadata,
        "total_occurrences": 0,
        "one": 0,
        "two": 0,
        "three": 0,
        "four": 0,
        "five": 0,
        "six": 0,
        "seven": 0,
        "eight": 0,
        "nine": 0,
        "ten": 0,
        "eleven": 0,
        "twelve": 0,
        "filter": 0,
        "optional": 0,
        "union": 0,
        "prop_path": 0,
        "group": 0,
        "bind": 0,
        "blank_node": 0,
        "minus": 0,
        "subselect": 0,
        "literal": 0,
        "values": 0,
        "service": 0,
        "other": 0}

    metadata_dict = {
        "data_type": metadata,
        "total_queries": 0,
        "SELECT_queries": 0,
        "DESCRIBE_queries": 0,
        "CONSTRUCT_queries": 0,
        "ASK_queries": 0,
        "found_scenarios": dict_looking_for
    }

    for datatype in datatype_list:
        # get the path to the folder, where the json file about the gathered statistical information
        # .. about the scenarios is stored (on the current datatype)
        # --> use the redundant / non redundant information here also
        path_to_stat_information_subtypes = "data/" + location[:21] + "/" + location[22:] + "/" + \
                                            datatype.split('/')[0] + "/statistical_information/" + \
                                            redundant_mode + "/" + datatype.split('/')[
                                                1]
        path_to_stat_information_metadata = "data/" + location[:21] + "/" + location[22:] + \
                                            "/statistical_information/" + redundant_mode + "/" + metadata + "/" \
                                            + metadata + ".json"

        # extract the statistical information
        with open(path_to_stat_information_subtypes, "r") as json_data:
            metadata_subtype_dict = json.load(json_data)

            # update the metadata_dict
            metadata_dict["total_queries"] += metadata_subtype_dict["total_queries"]
            metadata_dict["SELECT_queries"] += metadata_subtype_dict["SELECT_queries"]
            metadata_dict["DESCRIBE_queries"] += metadata_subtype_dict["DESCRIBE_queries"]
            metadata_dict["CONSTRUCT_queries"] += metadata_subtype_dict["CONSTRUCT_queries"]
            metadata_dict["ASK_queries"] += metadata_subtype_dict["ASK_queries"]

            for elem in metadata_subtype_dict["found_scenarios"]["list_per_search"]:
                metadata_dict["found_scenarios"]["total_occurrences"] += \
                    elem["total_occurrences"]
                metadata_dict["found_scenarios"]["one"] += \
                    elem["one"]
                metadata_dict["found_scenarios"]["two"] += \
                    elem["two"]
                metadata_dict["found_scenarios"]["three"] += \
                    elem["three"]
                metadata_dict["found_scenarios"]["four"] += \
                    elem["four"]
                metadata_dict["found_scenarios"]["five"] += \
                    elem["five"]
                metadata_dict["found_scenarios"]["six"] += \
                    elem["six"]
                metadata_dict["found_scenarios"]["seven"] += \
                    elem["seven"]
                metadata_dict["found_scenarios"]["eight"] += \
                    elem["eight"]
                metadata_dict["found_scenarios"]["nine"] += \
                    elem["nine"]
                metadata_dict["found_scenarios"]["ten"] += \
                    elem["ten"]
                metadata_dict["found_scenarios"]["eleven"] += \
                    elem["eleven"]
                metadata_dict["found_scenarios"]["twelve"] += \
                    elem["twelve"]
                metadata_dict["found_scenarios"]["bind"] += \
                    elem["bind"]
                metadata_dict["found_scenarios"]["blank_node"] += \
                    elem["blank_node"]
                metadata_dict["found_scenarios"]["filter"] += \
                    elem["filter"]
                metadata_dict["found_scenarios"]["group"] += \
                    elem["group"]
                metadata_dict["found_scenarios"]["literal"] += \
                    elem["literal"]
                metadata_dict["found_scenarios"]["minus"] += \
                    elem["minus"]
                metadata_dict["found_scenarios"]["optional"] += \
                    elem["optional"]
                metadata_dict["found_scenarios"]["prop_path"] += \
                    elem["prop_path"]
                metadata_dict["found_scenarios"]["service"] += \
                    elem["service"]
                metadata_dict["found_scenarios"]["subselect"] = \
                    elem["subselect"]
                metadata_dict["found_scenarios"]["union"] = \
                    elem["union"]
                metadata_dict["found_scenarios"]["values"] = \
                    elem["values"]
        json_data.close()

    with open(path_to_stat_information_metadata, "w") as json_result:
        json.dump(metadata_dict, json_result)
    json_result.close()


# summarize the statistical information about the different timeframes
def summarize_statistical_information_about_timeframes(locations, metadata, redundant_mode):
    # struct for the resulting .json object

    if metadata not in ["qualifier_metadata", "reference_metadata", "rank_metadata"]:
        error_message = "Not supported metadata mode: ", metadata
        raise Exception(error_message)

    if redundant_mode not in ["redundant", "non_redundant"]:
        error_message = "Not supported redundancy mode: ", redundant_mode
        raise Exception(error_message)

    dict_looking_for = {
        "looking_for": metadata,
        "total_occurrences": 0,
        "one": 0,
        "two": 0,
        "three": 0,
        "four": 0,
        "five": 0,
        "six": 0,
        "seven": 0,
        "eight": 0,
        "nine": 0,
        "ten": 0,
        "eleven": 0,
        "twelve": 0,
        "filter": 0,
        "optional": 0,
        "union": 0,
        "prop_path": 0,
        "group": 0,
        "bind": 0,
        "blank_node": 0,
        "minus": 0,
        "subselect": 0,
        "literal": 0,
        "values": 0,
        "service": 0,
        "other": 0}

    metadata_dict = {
        "data_type": metadata,
        "total_queries": 0,
        "SELECT_queries": 0,
        "DESCRIBE_queries": 0,
        "CONSTRUCT_queries": 0,
        "ASK_queries": 0,
        "found_scenarios": dict_looking_for
    }

    # 'location' e.g. "2017-06-12_2017-07-09_organic"
    for location in locations:
        # get the path to the folder, where the json file about the gathered statistical information
        # .. about the metadata is stored (on the current timeframe)

        path_to_stat_information_metadata = "data/" + location[:21] + "/" + location[22:] + \
                                            "/statistical_information/" + redundant_mode + "/" \
                                            + metadata + "/" + metadata + ".json"
        path_to_stat_information_timeframe = "data/statistical_information/query_research/" + redundant_mode + "/"\
                                             + metadata + "/" + metadata +".json"

        # extract the statistical information
        with open(path_to_stat_information_metadata, "r") as json_data:
            metadata_subtype_dict = json.load(json_data)

            # update the metadata_dict
            metadata_dict["total_queries"] += metadata_subtype_dict["total_queries"]
            metadata_dict["SELECT_queries"] += metadata_subtype_dict["SELECT_queries"]
            metadata_dict["DESCRIBE_queries"] += metadata_subtype_dict["DESCRIBE_queries"]
            metadata_dict["CONSTRUCT_queries"] += metadata_subtype_dict["CONSTRUCT_queries"]
            metadata_dict["ASK_queries"] += metadata_subtype_dict["ASK_queries"]

            elem = metadata_subtype_dict["found_scenarios"]

            metadata_dict["found_scenarios"]["total_occurrences"] += \
                elem["total_occurrences"]
            metadata_dict["found_scenarios"]["one"] += \
                elem["one"]
            metadata_dict["found_scenarios"]["two"] += \
                elem["two"]
            metadata_dict["found_scenarios"]["three"] += \
                elem["three"]
            metadata_dict["found_scenarios"]["four"] += \
                elem["four"]
            metadata_dict["found_scenarios"]["five"] += \
                elem["five"]
            metadata_dict["found_scenarios"]["six"] += \
                elem["six"]
            metadata_dict["found_scenarios"]["seven"] += \
                elem["seven"]
            metadata_dict["found_scenarios"]["eight"] += \
                elem["eight"]
            metadata_dict["found_scenarios"]["nine"] += \
                elem["nine"]
            metadata_dict["found_scenarios"]["ten"] += \
                elem["ten"]
            metadata_dict["found_scenarios"]["eleven"] += \
                elem["eleven"]
            metadata_dict["found_scenarios"]["twelve"] += \
                elem["twelve"]
            metadata_dict["found_scenarios"]["bind"] += \
                elem["bind"]
            metadata_dict["found_scenarios"]["blank_node"] += \
                elem["blank_node"]
            metadata_dict["found_scenarios"]["filter"] += \
                elem["filter"]
            metadata_dict["found_scenarios"]["group"] += \
                elem["group"]
            metadata_dict["found_scenarios"]["literal"] += \
                elem["literal"]
            metadata_dict["found_scenarios"]["minus"] += \
                elem["minus"]
            metadata_dict["found_scenarios"]["optional"] += \
                elem["optional"]
            metadata_dict["found_scenarios"]["prop_path"] += \
                elem["prop_path"]
            metadata_dict["found_scenarios"]["service"] += \
                elem["service"]
            metadata_dict["found_scenarios"]["subselect"] = \
                elem["subselect"]
            metadata_dict["found_scenarios"]["union"] = \
                elem["union"]
            metadata_dict["found_scenarios"]["values"] = \
                elem["values"]
        json_data.close()

    with open(path_to_stat_information_timeframe, "w") as json_result:
        json.dump(metadata_dict, json_result)
    json_result.close()


# summarize the counted properties for references / qualifiers in the timeframes to an overall one
def summarize_statistical_information_about_counted_properties(TIMEFRAMES, mode, redundant_mode):
    if mode not in ["qualifier_metadata", "reference_metadata"]:
        error_message = "Not supported mode: ", mode
        raise Exception(error_message)

    if redundant_mode not in ["redundant", "non_redundant"]:
        error_message = "Not supported redundancy mode: ", redundant_mode
        raise Exception(error_message)



    result_dict = {}
    result_dict["properties"] = {}
    result_dict["unique_properties"] = 0
    result_dict["total_properties"] = 0

    for location in TIMEFRAMES:

        path_to_timeframe_stat_information = "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" \
                                   + redundant_mode + "/" + mode + "/raw_counted_properties/properties_counted.json"
        with open(path_to_timeframe_stat_information, "r") as timeframe_data:
            timeframe_dict = json.load(timeframe_data)

            result_dict["total_properties"] += timeframe_dict["total_properties"]
            result_dict["unique_properties"] += timeframe_dict["unique_properties"]

            for PID in timeframe_dict["properties"]:
                if PID in result_dict["properties"]:
                    result_dict["properties"][PID] += timeframe_dict["properties"][PID]
                else:
                    result_dict["properties"][PID] = timeframe_dict["properties"][PID]

        timeframe_data.close()

    path_to_overall_stat_information = \
        "data/statistical_information/query_research/" + redundant_mode + "/" \
        + mode + "/raw_counted_properties/properties_counted.json"
    with open(path_to_overall_stat_information, "w") as result_data:
        json.dump(result_dict, result_data)


# get the top x counted properties in the counted properties list for references / qualifiers
def get_top_x_counted_properties_overall(x, mode, redundant_mode):
    if mode not in ["qualifier_metadata", "reference_metadata"]:
        error_message = "Not supported mode."
        raise Exception(error_message)
    if x < 1:
        error_message = "x must be greater than 0 - can only get the top x elements for x > 0"
        raise Exception(error_message)

    if redundant_mode not in ["redundant", "non_redundant"]:
        error_message = "Not supported redundancy mode: ", redundant_mode
        raise Exception(error_message)

    result_dict = {}

    path_to_stat_information = \
        "data/statistical_information/query_research/" + redundant_mode + "/" \
        + mode + "/raw_counted_properties/properties_counted.json"

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
        "data/statistical_information/query_research/" + redundant_mode + "/" + mode + "/raw_counted_properties/" \
                                                                              + "top_" + str(x) + "_properties_counted.json"
    with open(path_to_top_x_stat_information, "w") as result_data:
        json.dump(result_dict, result_data)


################# start here ---> count the best / default / deprecated ranks of the timeframes & overall
