import glob
import json
import os
import gzip
import csv
from urllib.parse import unquote_plus


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
        "total_scenarios": 0,
        "prop_one": 0,
        "prop_two": 0,
        "prop_three": 0,
        "prop_four": 0,
        "obj_one": 0,
        "obj_two": 0,
        "obj_three": 0,
        "obj_four": 0,
        "sub_one": 0,
        "sub_two": 0,
        "sub_three": 0,
        "sub_four": 0,
        "filter": 0,
        "optional": 0,
        "union": 0,
        "prop_path": 0,
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
                                                1] + ".json"
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
                metadata_dict["found_scenarios"]["total_scenarios"] += \
                    elem["total_scenarios"]
                metadata_dict["found_scenarios"]["prop_one"] += \
                    elem["prop_one"]
                metadata_dict["found_scenarios"]["prop_three"] += \
                    elem["prop_three"]
                metadata_dict["found_scenarios"]["prop_two"] += \
                    elem["prop_two"]
                metadata_dict["found_scenarios"]["prop_four"] += \
                    elem["prop_four"]
                metadata_dict["found_scenarios"]["obj_one"] += \
                    elem["obj_one"]
                metadata_dict["found_scenarios"]["obj_two"] += \
                    elem["obj_two"]
                metadata_dict["found_scenarios"]["obj_three"] += \
                    elem["obj_three"]
                metadata_dict["found_scenarios"]["obj_four"] += \
                    elem["obj_four"]
                metadata_dict["found_scenarios"]["sub_one"] += \
                    elem["sub_one"]
                metadata_dict["found_scenarios"]["sub_two"] += \
                    elem["sub_two"]
                metadata_dict["found_scenarios"]["sub_three"] += \
                    elem["sub_three"]
                metadata_dict["found_scenarios"]["sub_four"] += \
                    elem["sub_four"]
                metadata_dict["found_scenarios"]["bind"] += \
                    elem["bind"]
                metadata_dict["found_scenarios"]["blank_node"] += \
                    elem["blank_node"]
                metadata_dict["found_scenarios"]["filter"] += \
                    elem["filter"]
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
                metadata_dict["found_scenarios"]["union"] += \
                    elem["union"]
                metadata_dict["found_scenarios"]["subselect"] += \
                    elem["subselect"]
                metadata_dict["found_scenarios"]["values"] += \
                    elem["values"]
                metadata_dict["found_scenarios"]["other"] += \
                    elem["other"]
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
        "total_scenarios": 0,
        "prop_one": 0,
        "prop_two": 0,
        "prop_three": 0,
        "prop_four": 0,
        "obj_one": 0,
        "obj_two": 0,
        "obj_three": 0,
        "obj_four": 0,
        "sub_one": 0,
        "sub_two": 0,
        "sub_three": 0,
        "sub_four": 0,
        "filter": 0,
        "optional": 0,
        "union": 0,
        "prop_path": 0,
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
            metadata_dict["found_scenarios"]["total_scenarios"] += \
                elem["total_scenarios"]
            metadata_dict["found_scenarios"]["prop_one"] += \
                elem["prop_one"]
            metadata_dict["found_scenarios"]["prop_three"] += \
                elem["prop_three"]
            metadata_dict["found_scenarios"]["prop_two"] += \
                elem["prop_two"]
            metadata_dict["found_scenarios"]["prop_four"] += \
                elem["prop_four"]
            metadata_dict["found_scenarios"]["obj_one"] += \
                elem["obj_one"]
            metadata_dict["found_scenarios"]["obj_two"] += \
                elem["obj_two"]
            metadata_dict["found_scenarios"]["obj_three"] += \
                elem["obj_three"]
            metadata_dict["found_scenarios"]["obj_four"] += \
                elem["obj_four"]
            metadata_dict["found_scenarios"]["sub_one"] += \
                elem["sub_one"]
            metadata_dict["found_scenarios"]["sub_two"] += \
                elem["sub_two"]
            metadata_dict["found_scenarios"]["sub_three"] += \
                elem["sub_three"]
            metadata_dict["found_scenarios"]["sub_four"] += \
                elem["sub_four"]
            metadata_dict["found_scenarios"]["bind"] += \
                elem["bind"]
            metadata_dict["found_scenarios"]["blank_node"] += \
                elem["blank_node"]
            metadata_dict["found_scenarios"]["filter"] += \
                elem["filter"]
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
            metadata_dict["found_scenarios"]["union"] += \
                elem["union"]
            metadata_dict["found_scenarios"]["subselect"] += \
                elem["subselect"]
            metadata_dict["found_scenarios"]["values"] += \
                elem["values"]
            metadata_dict["found_scenarios"]["other"] += \
                elem["other"]

        json_data.close()

    with open(path_to_stat_information_timeframe, "w") as json_result:
        json.dump(metadata_dict, json_result)
    json_result.close()


# summarize the counted properties for references / qualifiers in the timeframes to an overall one
def summarize_statistical_information_about_counted_raw_properties(TIMEFRAMES, mode, redundant_mode):
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
def get_top_x_counted_raw_properties_overall(x, mode, redundant_mode):
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


# summarize the counted rank types in the timeframes to an overall one
def summarize_statistical_information_about_counted_ranks(TIMEFRAMES, mode, redundant_mode):
    if mode not in ["rank_metadata"]:
        error_message = "Not supported mode: ", mode
        raise Exception(error_message)

    if redundant_mode not in ["redundant", "non_redundant"]:
        error_message = "Not supported redundancy mode: ", redundant_mode
        raise Exception(error_message)

    result_dict = {}
    result_dict["ranks"] = {}
    result_dict["ranks"]["best_rank"] = 0
    result_dict["ranks"]["preferred_rank"] = 0
    result_dict["ranks"]["normal_rank"] = 0
    result_dict["ranks"]["deprecated_rank"] = 0
    result_dict["total_ranks"] = 0

    for location in TIMEFRAMES:

        path_to_timeframe_stat_information = "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" \
                                   + redundant_mode + "/" + mode + "/ranks_counted.json"
        with open(path_to_timeframe_stat_information, "r") as timeframe_data:
            timeframe_dict = json.load(timeframe_data)

            result_dict["total_ranks"] += timeframe_dict["total_ranks"]

            result_dict["ranks"]["best_rank"] += timeframe_dict["ranks"]["best_rank"]
            result_dict["ranks"]["preferred_rank"] += timeframe_dict["ranks"]["preferred_rank"]
            result_dict["ranks"]["normal_rank"] += timeframe_dict["ranks"]["normal_rank"]
            result_dict["ranks"]["deprecated_rank"] += timeframe_dict["ranks"]["deprecated_rank"]

        timeframe_data.close()

    path_to_overall_stat_information = \
        "data/statistical_information/query_research/" + redundant_mode + "/" \
        + mode + "/ranks_counted.json"

    with open(path_to_overall_stat_information, "w") as result_data:
        json.dump(result_dict, result_data)








# get the top x counted properties in the counted properties list for references / qualifiers in the current timeframe
# .. from the 'raw' counted properties
#
# .. and, if each property is recommended by Wikidata as a qualifier/reference property (depending on the 'mode')
# -- > which means, if the property is defined by Wikidata to be used as a property (see: 'Wikidata -> Proprties List')
# the data will be seperated by "recommended" properties, "non_recommended" properties and "overall" properties
#
# In the data, these recommendations will be visible through the information in the dict under "is_reference" or
# ..  if the "qualifier_class" contains any information
def get_top_x_counted_properties_timeframe(location, x, mode, recommended = None, redundant_mode = None):
    if mode not in ["qualifier_metadata", "reference_metadata"]:
        error_message = "Not supported mode: ", mode
        raise Exception(error_message)
    if redundant_mode not in ["redundant", "non_redundant"]:
        error_message = "Not supported redundancy mode: ", redundant_mode
        raise Exception(error_message)

    if x < 1:
        error_message = "x must be greater than 0 - can only get the top x elements for x > 0"
        raise Exception(error_message)

    result_dict = {}
    result_dict["properties"] = {}
    result_dict["total_properties"] = 0
    result_dict["unique_properties"] = 0


    props_dict = {}
    props_dict["properties"] = {}
    props_dict["total_properties"] = 0
    props_dict["unique_properties"] = 0


    if recommended is None:
        result_dict["total_false_properties"] = 0
        result_dict["unique_false_properties"] = 0
        props_dict["total_false_properties"] = 0
        props_dict["unique_false_properties"] = 0


    path_to_stat_information = "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" \
                                   + redundant_mode + "/" + mode + "/raw_counted_properties/properties_facets_and_datatypes.json"

    with open(path_to_stat_information, "r") as summarized_data:
        summarized_dict = json.load(summarized_data)

        # only display the total false properties on the "ALL" properties
        if recommended is None:
            props_dict["total_false_properties"] = summarized_dict["total_false_wikidata_property_usages"]
            props_dict["unique_false_properties"] = summarized_dict["unique_false_wikidata_property_usages"]

        for PID in summarized_dict["real_wikidata_properties"]:

            # check, if the property is /is not a recommended reference/qualifier by Wikidata
            recommended_bool = True

            if recommended == True:
                if mode == "reference_metadata":
                    recommended_bool = bool(summarized_dict["real_wikidata_properties"][PID]["is_reference"])
                elif mode == "qualifier_metadata":
                    recommended_bool = summarized_dict["real_wikidata_properties"][PID]["qualifier_class"] != []
                else:
                    recommended_bool = False

            elif recommended == False:
                # --> but they are min. 1x times used as a reference/qualifier, but not recommended
                if mode == "reference_metadata" and int(
                        summarized_dict["real_wikidata_properties"][PID]["occurrences"]) > 0 \
                        and not bool(summarized_dict["real_wikidata_properties"][PID]["is_reference"]):
                    recommended_bool = True
                # --> but they are min. 1x times used as a reference/qualifier, but not recommended
                elif mode == "qualifier_metadata" and int(
                        summarized_dict["real_wikidata_properties"][PID]["occurrences"]) > 0 \
                        and summarized_dict["real_wikidata_properties"][PID]["qualifier_class"] == []:
                    recommended_bool = True
                else:
                    recommended_bool = False

            elif recommended is None:
                # just exclude those, who either aren't a recommended qualifier/reference property
                # .. or are never used as a reference / qualifier
                if mode == "reference_metadata" and (
                        int(summarized_dict["real_wikidata_properties"][PID]["occurrences"]) > 0 \
                        or bool(summarized_dict["real_wikidata_properties"][PID]["is_reference"])):
                    recommended_bool = True
                elif mode == "qualifier_metadata" and (
                        int(summarized_dict["real_wikidata_properties"][PID]["occurrences"]) > 0 \
                        or summarized_dict["real_wikidata_properties"][PID]["qualifier_class"] != []):
                    recommended_bool = True
                else:
                    recommended_bool = False

            if recommended_bool:

                props_dict["properties"][PID] = \
                    summarized_dict["real_wikidata_properties"][PID]["occurrences"]
                props_dict["total_properties"] += \
                    summarized_dict["real_wikidata_properties"][PID]["occurrences"]
                props_dict["unique_properties"] += 1

    summarized_data.close()

    result_dict["unique_properties"] = props_dict["unique_properties"]
    result_dict["total_properties"] = props_dict["total_properties"]

    # only display the total false properties on the "ALL" properties
    if recommended is None:
        result_dict["total_false_properties"] = props_dict["total_false_properties"]
        result_dict["unique_false_properties"] = props_dict["unique_false_properties"]

    if recommended:
        tmp_string = "/recommended"
    elif recommended is not None:
        tmp_string = "/non_recommended"
    else:
        tmp_string = "/all"

    path_to_properties_stat_information = \
        "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" + redundant_mode + "/" + mode \
        + tmp_string + "/properties/properties.json"

    with open(path_to_properties_stat_information, "w") as result_data:
        json.dump(props_dict, result_data)

    # get the top x properties in the dictionary
    for property in props_dict["properties"]:

        if len(result_dict["properties"]) < x:
            result_dict["properties"][property] = props_dict["properties"][property]
        else:
            # get the smallest element out of the result_dict
            smallest_ID = None
            for test_PID in result_dict["properties"]:
                if smallest_ID is None:
                    smallest_ID = test_PID
                elif result_dict["properties"][test_PID] < result_dict["properties"][smallest_ID]:
                    smallest_ID = test_PID

            # if the current element of the raw_dict is greater than the smallest element of the result_dict
            # .. -> swap them in the result_dict
            if result_dict["properties"][smallest_ID] < props_dict["properties"][property]:
                result_dict["properties"].pop(smallest_ID)
                result_dict["properties"][property] = props_dict["properties"][property]

    result_data.close()


    if recommended:
        tmp_string = "/recommended"
    elif recommended is not None:
        tmp_string = "/non_recommended"
    else:
        tmp_string = "/all"

    path_to_top_x_stat_information = \
        "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" + redundant_mode + "/" \
        + mode + tmp_string + "/properties/"\
        + "top_" + str(x) + "_properties.json"


    with open(path_to_top_x_stat_information, "w") as result_data:
        json.dump(result_dict, result_data)



# get the top x counted facets in the counted properties list for references / qualifiers in the current timeframe
# .. and, if each property is recommended by Wikidata as a qualifier/reference property (depending on the 'mode')
# -- > which means, if the property is defined by Wikidata to be used as a property (see: 'Wikidata -> Proprties List')
# the data will be seperated by "recommended" properties, "non_recommended" properties and "overall" properties
#
# In the data, these recommendations will be visible through the information in the dict under "is_reference" or
# ..  if the "qualifier_class" contains any information
def get_top_x_counted_facets_timeframe(location, x, mode, recommended = None, redundant_mode = None):
    if mode not in ["qualifier_metadata", "reference_metadata"]:
        error_message = "Not supported mode: ", mode
        raise Exception(error_message)
    if x < 1:
        error_message = "x must be greater than 0 - can only get the top x elements for x > 0"
        raise Exception(error_message)
    if redundant_mode not in ["redundant", "non_redundant"]:
        error_message = "Not supported redundancy mode: ", redundant_mode
        raise Exception(error_message)

    result_dict = {}
    result_dict["facets"] = {}
    result_dict["total_facet"] = 0
    result_dict["unique_facets"] = 0
    result_dict["properties_without_facets"] = 0

    facet_dict = {}
    facet_dict["facets"] = {}
    facet_dict["total_facets"] = 0
    facet_dict["unique_facets"] = 0
    facet_dict["properties_without_facets"] = 0

    path_to_stat_information = "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" \
                                   + redundant_mode + "/" + mode + "/raw_counted_properties/properties_facets_and_datatypes.json"

    with open(path_to_stat_information, "r") as summarized_data:
        summarized_dict = json.load(summarized_data)

        # create a facet dictionary
        for PID in summarized_dict["real_wikidata_properties"]:

            # check, if the property is /is not a recommended reference/qualifier by Wikidata
            recommended_bool = True

            if recommended == True:
                if mode == "reference_metadata":
                    recommended_bool = bool(summarized_dict["real_wikidata_properties"][PID]["is_reference"])
                elif mode == "qualifier_metadata":
                    recommended_bool = summarized_dict["real_wikidata_properties"][PID]["qualifier_class"] != []
                else:
                    recommended_bool = False

            elif recommended == False:
                # --> but they are min. 1x times used as a reference/qualifier, but not recommended
                if mode == "reference_metadata" and int(summarized_dict["real_wikidata_properties"][PID]["occurrences"]) > 0\
                        and not bool(summarized_dict["real_wikidata_properties"][PID]["is_reference"]):
                    recommended_bool = True
                # --> but they are min. 1x times used as a reference/qualifier, but not recommended
                elif mode == "qualifier_metadata" and int(summarized_dict["real_wikidata_properties"][PID]["occurrences"]) > 0\
                        and summarized_dict["real_wikidata_properties"][PID]["qualifier_class"] == []:
                    recommended_bool = True
                else:
                    recommended_bool = False

            elif recommended is None:
                # just exclude those, who either aren't a recommended qualifier/reference property
                # .. or are never used as a reference / qualifier
                if mode == "reference_metadata" and (int(summarized_dict["real_wikidata_properties"][PID]["occurrences"]) > 0\
                        or bool(summarized_dict["real_wikidata_properties"][PID]["is_reference"])):
                    recommended_bool = True
                elif mode == "qualifier_metadata" and (int(summarized_dict["real_wikidata_properties"][PID]["occurrences"]) > 0\
                        or summarized_dict["real_wikidata_properties"][PID]["qualifier_class"] != []):
                    recommended_bool = True
                else:
                    recommended_bool = False

            if recommended_bool:

                for facet in summarized_dict["real_wikidata_properties"][PID]["facets"]:

                    if (facet not in facet_dict["facets"]):
                        facet_dict["facets"][facet] = 1
                        facet_dict["total_facets"] += 1
                        facet_dict["unique_facets"] += 1
                    else:
                        facet_dict["facets"][facet] += 1
                        facet_dict["total_facets"] += 1

                # if the property does not have any facet superclasses, count the property usage by itself
                if len(summarized_dict["real_wikidata_properties"][PID]["facets"]) == 0:

                    if PID not in facet_dict["facets"]:
                        facet_dict["facets"][PID] = 1
                        facet_dict["properties_without_facets"] += 1
                    else:
                        facet_dict["facets"][PID] += 1
                        facet_dict["properties_without_facets"] += 1

        result_dict["unique_facets"] = facet_dict["unique_facets"]
        result_dict["total_facet"] = facet_dict["total_facets"]
        result_dict["properties_without_facets"] = facet_dict["properties_without_facets"]

        if recommended:
            tmp_string = "/recommended"
        elif recommended is not None:
            tmp_string = "/non_recommended"
        else:
            tmp_string = "/all"

        path_to_facet_stat_information = \
            "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" + redundant_mode + "/" + mode\
            + tmp_string + "/facets/facets.json"

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

    if recommended:
        tmp_string = "/recommended"
    elif recommended is not None:
        tmp_string = "/non_recommended"
    else:
        tmp_string = "/all"

    path_to_top_x_stat_information = \
        "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" + redundant_mode + "/" \
        + mode + tmp_string + "/facets/"\
        + "top_" + str(x) + "_facets.json"

    with open(path_to_top_x_stat_information, "w") as result_data:
        json.dump(result_dict, result_data)


# get the top x counted datytypes in the counted properties list for references / qualifiers in the current timeframe
#
# usage of 'recommended' as see above
def get_top_x_counted_datatypes_timeframe(location, x, mode, recommended = None, redundant_mode = None):
    if mode not in ["qualifier_metadata", "reference_metadata"]:
        error_message = "Not supported mode: ", mode
        raise Exception(error_message)
    if x < 1:
        error_message = "x must be greater than 0 - can only get the top x elements for x > 0"
        raise Exception(error_message)
    if redundant_mode not in ["redundant", "non_redundant"]:
        error_message = "Not supported redundancy mode: ", redundant_mode
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
                                   + redundant_mode + "/" + mode + "/raw_counted_properties/properties_facets_and_datatypes.json"

    with open(path_to_stat_information, "r") as summarized_data:
        summarized_dict = json.load(summarized_data)

        # create a datatypes dictionary
        for PID in summarized_dict["real_wikidata_properties"]:

            # check, if the property is /is not a recommended reference/qualifier by Wikidata
            recommended_bool = True

            if recommended == True:
                if mode == "reference_metadata":
                    recommended_bool = bool(summarized_dict["real_wikidata_properties"][PID]["is_reference"])
                elif mode == "qualifier_metadata":
                    recommended_bool = summarized_dict["real_wikidata_properties"][PID]["qualifier_class"] != []
                else:
                    recommended_bool = False

            elif recommended == False:
                # --> but they are min. 1x times used as a reference/qualifier, but not recommended
                if mode == "reference_metadata" and int(summarized_dict["real_wikidata_properties"][PID]["occurrences"]) > 0\
                        and not bool(summarized_dict["real_wikidata_properties"][PID]["is_reference"]):
                    recommended_bool = True
                # --> but they are min. 1x times used as a reference/qualifier, but not recommended
                elif mode == "qualifier_metadata" and int(summarized_dict["real_wikidata_properties"][PID]["occurrences"]) > 0\
                        and summarized_dict["real_wikidata_properties"][PID]["qualifier_class"] == []:
                    recommended_bool = True
                else:
                    recommended_bool = False

            elif recommended is None:
                # just exclude those, who either aren't a recommended qualifier/reference property
                # .. or are never used as a reference / qualifier
                if mode == "reference_metadata" and (int(summarized_dict["real_wikidata_properties"][PID]["occurrences"]) > 0\
                        or bool(summarized_dict["real_wikidata_properties"][PID]["is_reference"])):
                    recommended_bool = True
                elif mode == "qualifier_metadata" and (int(summarized_dict["real_wikidata_properties"][PID]["occurrences"]) > 0\
                        or summarized_dict["real_wikidata_properties"][PID]["qualifier_class"] != []):
                    recommended_bool = True
                else:
                    recommended_bool = False

            if recommended_bool:

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

        if recommended:
            tmp_string = "/recommended"
        elif recommended is not None:
            tmp_string = "/non_recommended"
        else:
            tmp_string = "/all"

        path_to_facet_stat_information = \
            "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" + redundant_mode + "/" + mode  \
            + tmp_string + "/datatypes/datatypes.json"

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

    if recommended:
        tmp_string = "/recommended"
    elif recommended is not None:
        tmp_string = "/non_recommended"
    else:
        tmp_string = "/all"

    path_to_top_x_stat_information = \
        "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" + redundant_mode + "/" + mode + tmp_string + \
        "/datatypes/top_" + str(x) + "_datatypes.json"

    with open(path_to_top_x_stat_information, "w") as result_data:
        json.dump(result_dict, result_data)


# get the top x accumulated facets in the counted properties list for references / qualifiers
# .. in the current timeframe
#
# usage of 'recommended' as explained above
def get_top_x_counted_accumulated_facets_timeframe(location, x, mode, recommended = None, redundant_mode = None):
    if mode not in ["qualifier_metadata", "reference_metadata"]:
        error_message = "Not supported mode: ", mode
        raise Exception(error_message)
    if x < 1:
        error_message = "x must be greater than 0 - can only get the top x elements for x > 0"
        raise Exception(error_message)
    if redundant_mode not in ["redundant", "non_redundant"]:
        error_message = "Not supported redundancy mode: ", redundant_mode
        raise Exception(error_message)

    result_dict = {}
    result_dict["facets"] = {}
    result_dict["total_accumulated_facet"] = 0
    result_dict["unique_facets"] = 0
    result_dict["properties_without_facets"] = 0
    result_dict["properties_without_facets_accumulated"] = 0

    facet_dict = {}
    facet_dict["facets"] = {}
    facet_dict["total_accumulated_facets"] = 0
    facet_dict["unique_facets"] = 0
    facet_dict["properties_without_facets"] = 0
    facet_dict["properties_without_facets_accumulated"] = 0

    path_to_stat_information = "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" \
                                   + redundant_mode + "/" + mode + "/raw_counted_properties/properties_facets_and_datatypes.json"

    with open(path_to_stat_information, "r") as summarized_data:
        summarized_dict = json.load(summarized_data)

        # create a facet dictionary
        for PID in summarized_dict["real_wikidata_properties"]:

            # check, if the property is /is not a recommended reference/qualifier by Wikidata
            recommended_bool = True

            if recommended == True:
                if mode == "reference_metadata":
                    recommended_bool = bool(summarized_dict["real_wikidata_properties"][PID]["is_reference"])
                elif mode == "qualifier_metadata":
                    recommended_bool = summarized_dict["real_wikidata_properties"][PID]["qualifier_class"] != []
                else:
                    recommended_bool = False

            elif recommended == False:
                # --> but they are min. 1x times used as a reference/qualifier, but not recommended
                if mode == "reference_metadata" and int(summarized_dict["real_wikidata_properties"][PID]["occurrences"]) > 0\
                        and not bool(summarized_dict["real_wikidata_properties"][PID]["is_reference"]):
                    recommended_bool = True
                # --> but they are min. 1x times used as a reference/qualifier, but not recommended
                elif mode == "qualifier_metadata" and int(summarized_dict["real_wikidata_properties"][PID]["occurrences"]) > 0\
                        and summarized_dict["real_wikidata_properties"][PID]["qualifier_class"] == []:
                    recommended_bool = True
                else:
                    recommended_bool = False

            elif recommended is None:
                # just exclude those, who either aren't a recommended qualifier/reference property
                # .. or are never used as a reference / qualifier
                if mode == "reference_metadata" and (int(summarized_dict["real_wikidata_properties"][PID]["occurrences"]) > 0\
                        or bool(summarized_dict["real_wikidata_properties"][PID]["is_reference"])):
                    recommended_bool = True
                elif mode == "qualifier_metadata" and (int(summarized_dict["real_wikidata_properties"][PID]["occurrences"]) > 0\
                        or summarized_dict["real_wikidata_properties"][PID]["qualifier_class"] != []):
                    recommended_bool = True
                else:
                    recommended_bool = False

            if recommended_bool:

                for facet in summarized_dict["real_wikidata_properties"][PID]["facets"]:

                    if (facet not in facet_dict["facets"]):
                        facet_dict["facets"][facet] = \
                            summarized_dict["real_wikidata_properties"][PID]["occurrences"]
                        facet_dict["total_accumulated_facets"] += \
                            summarized_dict["real_wikidata_properties"][PID]["occurrences"]
                        facet_dict["unique_facets"] += 1
                    else:
                        facet_dict["facets"][facet] += \
                            summarized_dict["real_wikidata_properties"][PID]["occurrences"]
                        facet_dict["total_accumulated_facets"] += \
                            summarized_dict["real_wikidata_properties"][PID]["occurrences"]

                # if the property does not have any facet superclasses, count the property usage by itself
                if len(summarized_dict["real_wikidata_properties"][PID]["facets"]) == 0:

                    if PID not in facet_dict["facets"]:
                        facet_dict["facets"][PID] = summarized_dict["real_wikidata_properties"][PID]["occurrences"]
                        facet_dict["properties_without_facets"] += 1
                        facet_dict["properties_without_facets_accumulated"] += \
                            summarized_dict["real_wikidata_properties"][PID]["occurrences"]
                    else:
                        facet_dict["facets"][PID] += summarized_dict["real_wikidata_properties"][PID]["occurrences"]
                        facet_dict["properties_without_facets_accumulated"] += \
                            summarized_dict["real_wikidata_properties"][PID]["occurrences"]

        result_dict["unique_facets"] = facet_dict["unique_facets"]
        result_dict["total_accumulated_facet"] = facet_dict["total_accumulated_facets"]
        result_dict["properties_without_facets"] = facet_dict["properties_without_facets"]
        result_dict["properties_without_facets_accumulated"] = facet_dict["properties_without_facets_accumulated"]

        if recommended:
            tmp_string = "/recommended"
        elif recommended is not None:
            tmp_string = "/non_recommended"
        else:
            tmp_string = "/all"

        path_to_facet_stat_information = \
            "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" + redundant_mode + "/" + mode \
            + tmp_string + "/accumulated_facets/accumulated_facets.json"

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

        if recommended:
            tmp_string = "/recommended"
        elif recommended is not None:
            tmp_string = "/non_recommended"
        else:
            tmp_string = "/all"

    path_to_top_x_stat_information = \
        "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" + redundant_mode + "/" + mode + tmp_string +\
        "/accumulated_facets/top_" + str(x) + "_accumulated_facets.json"

    with open(path_to_top_x_stat_information, "w") as result_data:
        json.dump(result_dict, result_data)


# get the top x accumulated datytypes in the counted properties list for references / qualifiers
# .. in the current timeframe
#
# usage of 'recommended' as described above
def get_top_x_counted_accumulated_datatypes_timeframe(location, x, mode, recommended = None, redundant_mode = None):
    if mode not in ["qualifier_metadata", "reference_metadata"]:
        error_message = "Not supported mode: ", mode
        raise Exception(error_message)
    if x < 1:
        error_message = "x must be greater than 0 - can only get the top x elements for x > 0"
        raise Exception(error_message)
    if redundant_mode not in ["redundant", "non_redundant"]:
        error_message = "Not supported redundancy mode: ", redundant_mode
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
                                   + redundant_mode + "/" +  mode + "/raw_counted_properties/properties_facets_and_datatypes.json"

    with open(path_to_stat_information, "r") as summarized_data:
        summarized_dict = json.load(summarized_data)

        # create a datatypes dictionary
        for PID in summarized_dict["real_wikidata_properties"]:

            # check, if the property is /is not a recommended reference/qualifier by Wikidata
            recommended_bool = True

            if recommended == True:
                if mode == "reference_metadata":
                    recommended_bool = bool(summarized_dict["real_wikidata_properties"][PID]["is_reference"])
                elif mode == "qualifier_metadata":
                    recommended_bool = summarized_dict["real_wikidata_properties"][PID]["qualifier_class"] != []
                else:
                    recommended_bool = False

            elif recommended == False:
                # --> but they are min. 1x times used as a reference/qualifier, but not recommended
                if mode == "reference_metadata" and int(summarized_dict["real_wikidata_properties"][PID]["occurrences"]) > 0 \
                        and not bool(summarized_dict["real_wikidata_properties"][PID]["is_reference"]):
                    recommended_bool = True
                # --> but they are min. 1x times used as a reference/qualifier, but not recommended
                elif mode == "qualifier_metadata" and int(summarized_dict["real_wikidata_properties"][PID]["occurrences"]) > 0 \
                        and summarized_dict["real_wikidata_properties"][PID]["qualifier_class"] == []:
                    recommended_bool = True
                else:
                    recommended_bool = False

            elif recommended is None:
                # just exclude those, who either aren't a recommended qualifier/reference property
                # .. or are never used as a reference / qualifier
                if mode == "reference_metadata" and (int(summarized_dict["real_wikidata_properties"][PID]["occurrences"]) > 0 \
                                            or bool(
                            summarized_dict["real_wikidata_properties"][PID]["is_reference"])):
                    recommended_bool = True
                elif mode == "qualifier_metadata" and (
                        int(summarized_dict["real_wikidata_properties"][PID]["occurrences"]) > 0 \
                        or summarized_dict["real_wikidata_properties"][PID]["qualifier_class"] != []):
                    recommended_bool = True
                else:
                    recommended_bool = False

            if recommended_bool:

                datatype = summarized_dict["real_wikidata_properties"][PID]["datatype"]

                if (datatype not in datatype_dict["datatypes"]):
                    datatype_dict["datatypes"][datatype] = \
                            summarized_dict["real_wikidata_properties"][PID]["occurrences"]
                    datatype_dict["total_accumulated_datatypes"] += \
                            summarized_dict["real_wikidata_properties"][PID]["occurrences"]
                    datatype_dict["unique_datatypes"] += 1
                else:
                    datatype_dict["datatypes"][datatype] += \
                            summarized_dict["real_wikidata_properties"][PID]["occurrences"]
                    datatype_dict["total_accumulated_datatypes"] += \
                            summarized_dict["real_wikidata_properties"][PID]["occurrences"]

        result_dict["unique_datatypes"] = datatype_dict["unique_datatypes"]
        result_dict["total_accumulated_datatypes"] = datatype_dict["total_accumulated_datatypes"]

        if recommended:
            tmp_string = "/recommended"
        elif recommended is not None:
            tmp_string = "/non_recommended"
        else:
            tmp_string = "/all"

        path_to_facet_stat_information = \
            "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" + redundant_mode + "/" + mode \
            + tmp_string + "/accumulated_datatypes/accumulated_datatypes.json"

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

        if recommended:
            tmp_string = "/recommended"
        elif recommended is not None:
            tmp_string = "/non_recommended"
        else:
            tmp_string = "/all"

    path_to_top_x_stat_information = \
        "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" + redundant_mode + "/" + mode + tmp_string + \
        "/accumulated_datatypes/top_" + str(x) + "_accumulated_datatypes.json"

    with open(path_to_top_x_stat_information, "w") as result_data:
        json.dump(result_dict, result_data)



# summarize the information of the timeframes about the used recommended/non recommended properties to an overall one
# .. and get the top x used properties
def summarize_timeframe_information_about_properties_and_get_top_x(x, locations, mode, recommended_mode = None, redundant_mode = None):
    if mode not in ["qualifier_metadata", "reference_metadata"]:
        error_message = "Not supported mode."
        raise Exception(error_message)

    if x < 1:
        error_message = "x must be greater than 0 - can only get the top x elements for x > 0"
        raise Exception(error_message)

    if redundant_mode not in ["redundant", "non_redundant"]:
        error_message = "Not supported redundancy mode: ", redundant_mode
        raise Exception(error_message)

    props_dict = {}
    props_dict["properties"] = {}
    props_dict["total_properties"] = 0
    props_dict["unique_properties"] = 0

    result_dict = {}
    result_dict["properties"] = {}
    result_dict["total_properties"] = 0
    result_dict["unique_properties"] = 0

    # only display the total false properties on the "ALL" properties
    if recommended_mode is None:
        props_dict["total_false_properties"] = 0
        result_dict["total_false_properties"] = 0


    for location in locations:

        if recommended_mode:
            tmp_string = "/recommended"
        elif recommended_mode is not None:
            tmp_string = "/non_recommended"
        else:
            tmp_string = "/all"

        path_to_properties_stat_information_timeframe = \
            "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" + redundant_mode + "/" + mode \
            + tmp_string + "/properties/properties.json"


        with open(path_to_properties_stat_information_timeframe, "r") as timeframe_data:
            timeframe_dict = json.load(timeframe_data)

            props_dict["total_properties"] += timeframe_dict["total_properties"]

            # only display the total false properties on the "ALL" properties
            if recommended_mode is None:
                props_dict["total_false_properties"] += timeframe_dict["total_false_properties"]

            for PID in timeframe_dict["properties"]:

                if PID in props_dict["properties"]:
                    props_dict["properties"][PID] += timeframe_dict["properties"][PID]
                else:
                    props_dict["properties"][PID] = timeframe_dict["properties"][PID]
                    props_dict["unique_properties"] += 1

        if recommended_mode:
            tmp_string = "/recommended"
        elif recommended_mode is not None:
            tmp_string = "/non_recommended"
        else:
            tmp_string = "/all"

    path_to_properties_stat_information_overall = \
        "data/statistical_information/query_research/" + redundant_mode + "/" + mode \
        + tmp_string + "/properties/properties.json"

    with open(path_to_properties_stat_information_overall, "w") as result_data:
        json.dump(props_dict, result_data)

        result_data.close()

    result_dict["total_properties"] = props_dict["total_properties"]
    result_dict["unique_properties"] = props_dict["unique_properties"]

    # only display the total false properties on the "ALL" properties
    if recommended_mode is None:
        result_dict["total_false_properties"] = props_dict["total_false_properties"]

    # get the top x properties in the ormer created dictionary
    for property in props_dict["properties"]:

        if len(result_dict["properties"]) < x:
            result_dict["properties"][property] = props_dict["properties"][property]
        else:
            # get the smallest element out of the result_dict
            smallest_ID = None
            for test_PID in result_dict["properties"]:
                if smallest_ID is None:
                    smallest_ID = test_PID
                elif result_dict["properties"][test_PID] < result_dict["properties"][smallest_ID]:
                    smallest_ID = test_PID

            # if the current element of the raw_dict is greater than the smallest element of the result_dict
            # .. -> swap them in the result_dict
            if result_dict["properties"][smallest_ID] < props_dict["properties"][property]:
                result_dict["properties"].pop(smallest_ID)
                result_dict["properties"][property] = props_dict["properties"][property]

    result_data.close()

    if recommended_mode:
        tmp_string = "/recommended"
    elif recommended_mode is not None:
        tmp_string = "/non_recommended"
    else:
        tmp_string = "/all"

    path_to_top_x_stat_information = \
        "data/statistical_information/query_research/" + redundant_mode + "/" \
        + mode + tmp_string + "/properties/" \
        + "top_" + str(x) + "_properties.json"

    with open(path_to_top_x_stat_information, "w") as result_data:
        json.dump(result_dict, result_data)
        result_data.close()


# summarize the information of the timeframes about the facets of the used recommended/non recommended properties
# .. to an overall one
# .. and get the top x used properties
def summarize_timeframe_information_about_facets_and_get_top_x(x, locations, mode, recommended_mode = None, redundant_mode = None):
    if mode not in ["qualifier_metadata", "reference_metadata"]:
        error_message = "Not supported mode."
        raise Exception(error_message)

    if x < 1:
        error_message = "x must be greater than 0 - can only get the top x elements for x > 0"
        raise Exception(error_message)

    if redundant_mode not in ["redundant", "non_redundant"]:
        error_message = "Not supported redundancy mode: ", redundant_mode
        raise Exception(error_message)

    facets_dict = {}
    facets_dict["facets"] = {}
    facets_dict["total_facets"] = 0
    facets_dict["unique_facets"] = 0

    result_dict = {}
    result_dict["facets"] = {}
    result_dict["total_facets"] = 0
    result_dict["unique_facets"] = 0

    for location in locations:

        if recommended_mode:
            tmp_string = "/recommended"
        elif recommended_mode is not None:
            tmp_string = "/non_recommended"
        else:
            tmp_string = "/all"

        path_to_facets_stat_information_timeframe = \
            "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" + redundant_mode + "/" + mode \
            + tmp_string + "/facets/facets.json"


        with open(path_to_facets_stat_information_timeframe, "r") as timeframe_data:
            timeframe_dict = json.load(timeframe_data)

            facets_dict["total_facets"] += timeframe_dict["total_facets"]

            for facet in timeframe_dict["facets"]:

                if facet in facets_dict["facets"]:
                    facets_dict["facets"][facet] += timeframe_dict["facets"][facet]
                else:
                    facets_dict["facets"][facet] = timeframe_dict["facets"][facet]
                    facets_dict["unique_facets"] += 1

        if recommended_mode:
            tmp_string = "/recommended"
        elif recommended_mode is not None:
            tmp_string = "/non_recommended"
        else:
            tmp_string = "/all"

    path_to_facets_stat_information_overall = \
        "data/statistical_information/query_research/" + redundant_mode + "/" + mode \
        + tmp_string + "/facets/facets.json"

    with open(path_to_facets_stat_information_overall, "w") as result_data:
        json.dump(facets_dict, result_data)

        result_data.close()

    result_dict["total_facets"] = facets_dict["total_facets"]
    result_dict["unique_facets"] = facets_dict["unique_facets"]

    # get the top x used facets in the former created dictionary
    for facet in facets_dict["facets"]:

        if len(result_dict["facets"]) < x:
            result_dict["facets"][facet] = facets_dict["facets"][facet]
        else:
            # get the smallest element out of the result_dict
            smallest_ID = None
            for test_PID in result_dict["facets"]:
                if smallest_ID is None:
                    smallest_ID = test_PID
                elif result_dict["facets"][test_PID] < result_dict["facets"][smallest_ID]:
                    smallest_ID = test_PID

            # if the current element of the raw_dict is greater than the smallest element of the result_dict
            # .. -> swap them in the result_dict
            if result_dict["facets"][smallest_ID] < facets_dict["facets"][facet]:
                result_dict["facets"].pop(smallest_ID)
                result_dict["facets"][facet] = facets_dict["facets"][facet]

    result_data.close()

    if recommended_mode:
        tmp_string = "/recommended"
    elif recommended_mode is not None:
        tmp_string = "/non_recommended"
    else:
        tmp_string = "/all"

    path_to_top_x_stat_information = \
        "data/statistical_information/query_research/" + redundant_mode + "/" \
        + mode + tmp_string + "/facets/" \
        + "top_" + str(x) + "_facets.json"

    with open(path_to_top_x_stat_information, "w") as result_data:
        json.dump(result_dict, result_data)
        result_data.close()


# summarize the information of the timeframes about the datatypes of the used recommended/non recommended properties
# .. to an overall one
def summarize_timeframe_information_about_datatypes(locations, mode, recommended_mode = None, redundant_mode = None):
    if mode not in ["qualifier_metadata", "reference_metadata"]:
        error_message = "Not supported mode."
        raise Exception(error_message)

    if redundant_mode not in ["redundant", "non_redundant"]:
        error_message = "Not supported redundancy mode: ", redundant_mode
        raise Exception(error_message)

    datatypes_dict = {}
    datatypes_dict["datatypes"] = {}
    datatypes_dict["total_datatypes"] = 0
    datatypes_dict["unique_datatypes"] = 0

    result_dict = {}
    result_dict["datatypes"] = {}
    result_dict["total_datatypes"] = 0
    result_dict["unique_datatypes"] = 0


    for location in locations:

        if recommended_mode:
            tmp_string = "/recommended"
        elif recommended_mode is not None:
            tmp_string = "/non_recommended"
        else:
            tmp_string = "/all"

        path_to_datatypes_stat_information_timeframe = \
            "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" + redundant_mode + "/" + mode \
            + tmp_string + "/datatypes/datatypes.json"


        with open(path_to_datatypes_stat_information_timeframe, "r") as timeframe_data:
            timeframe_dict = json.load(timeframe_data)

            datatypes_dict["total_datatypes"] += timeframe_dict["total_datatypes"]

            for datatype in timeframe_dict["datatypes"]:

                if datatype in datatypes_dict["datatypes"]:
                    datatypes_dict["datatypes"][datatype] += timeframe_dict["datatypes"][datatype]
                else:
                    datatypes_dict["datatypes"][datatype] = timeframe_dict["datatypes"][datatype]
                    datatypes_dict["unique_datatypes"] += 1

        if recommended_mode:
            tmp_string = "/recommended"
        elif recommended_mode is not None:
            tmp_string = "/non_recommended"
        else:
            tmp_string = "/all"

    path_to_datatypes_stat_information_overall = \
        "data/statistical_information/query_research/" + redundant_mode + "/" + mode \
        + tmp_string + "/datatypes/datatypes.json"

    with open(path_to_datatypes_stat_information_overall, "w") as result_data:
        json.dump(datatypes_dict, result_data)

        result_data.close()


# summarize the information of the timeframes about the accumulated facets of the used recommended/non recommended properties
# .. to an overall one
# .. and get the top x used properties
def summarize_timeframe_information_about_accumulated_facets_and_get_top_x(x, locations, mode, recommended_mode = None, redundant_mode = None):
    if mode not in ["qualifier_metadata", "reference_metadata"]:
        error_message = "Not supported mode."
        raise Exception(error_message)

    if x < 1:
        error_message = "x must be greater than 0 - can only get the top x elements for x > 0"
        raise Exception(error_message)

    if redundant_mode not in ["redundant", "non_redundant"]:
        error_message = "Not supported redundancy mode: ", redundant_mode
        raise Exception(error_message)

    facets_dict = {}
    facets_dict["facets"] = {}
    facets_dict["total_accumulated_facets"] = 0
    facets_dict["unique_facets"] = 0
    facets_dict["properties_without_facets_accumulated"] = 0

    result_dict = {}
    result_dict["facets"] = {}
    result_dict["total_accumulated_facets"] = 0
    result_dict["unique_facets"] = 0
    result_dict["properties_without_facets_accumulated"] = 0

    for location in locations:

        if recommended_mode:
            tmp_string = "/recommended"
        elif recommended_mode is not None:
            tmp_string = "/non_recommended"
        else:
            tmp_string = "/all"

        path_to_accumulated_facets_stat_information_timeframe = \
            "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" + redundant_mode + "/" + mode \
            + tmp_string + "/accumulated_facets/accumulated_facets.json"


        with open(path_to_accumulated_facets_stat_information_timeframe, "r") as timeframe_data:
            timeframe_dict = json.load(timeframe_data)

            facets_dict["total_accumulated_facets"] += timeframe_dict["total_accumulated_facets"]
            facets_dict["properties_without_facets_accumulated"] += timeframe_dict["properties_without_facets_accumulated"]

            for facet in timeframe_dict["facets"]:

                if facet in facets_dict["facets"]:
                    facets_dict["facets"][facet] += timeframe_dict["facets"][facet]
                else:
                    facets_dict["facets"][facet] = timeframe_dict["facets"][facet]
                    facets_dict["unique_facets"] += 1

        if recommended_mode:
            tmp_string = "/recommended"
        elif recommended_mode is not None:
            tmp_string = "/non_recommended"
        else:
            tmp_string = "/all"

    path_to_accumulated_facets_stat_information_overall = \
        "data/statistical_information/query_research/" + redundant_mode + "/" + mode \
        + tmp_string + "/accumulated_facets/accumulated_facets.json"

    with open(path_to_accumulated_facets_stat_information_overall, "w") as result_data:
        json.dump(facets_dict, result_data)

        result_data.close()

    result_dict["total_accumulated_facets"] = facets_dict["total_accumulated_facets"]
    result_dict["unique_facets"] = facets_dict["unique_facets"]
    result_dict["properties_without_facets_accumulated"] = facets_dict["properties_without_facets_accumulated"]

    # get the top x accumulated facets in the former created dictionary
    for facet in facets_dict["facets"]:

        if len(result_dict["facets"]) < x:
            result_dict["facets"][facet] = facets_dict["facets"][facet]
        else:
            # get the smallest element out of the result_dict
            smallest_ID = None
            for test_PID in result_dict["facets"]:
                if smallest_ID is None:
                    smallest_ID = test_PID
                elif result_dict["facets"][test_PID] < result_dict["facets"][smallest_ID]:
                    smallest_ID = test_PID

            # if the current element of the raw_dict is greater than the smallest element of the result_dict
            # .. -> swap them in the result_dict
            if result_dict["facets"][smallest_ID] < facets_dict["facets"][facet]:
                result_dict["facets"].pop(smallest_ID)
                result_dict["facets"][facet] = facets_dict["facets"][facet]

    result_data.close()

    if recommended_mode:
        tmp_string = "/recommended"
    elif recommended_mode is not None:
        tmp_string = "/non_recommended"
    else:
        tmp_string = "/all"

    path_to_top_x_stat_information = \
        "data/statistical_information/query_research/" + redundant_mode + "/" \
        + mode + tmp_string + "/accumulated_facets/" \
        + "top_" + str(x) + "_accumulated_facets.json"

    with open(path_to_top_x_stat_information, "w") as result_data:
        json.dump(result_dict, result_data)
        result_data.close()


# summarize the information of the timeframes about the accumulated datatypes
# .. of the used recommended/non recommended properties
# .. to an overall one
def summarize_timeframe_information_about_accumulated_datatypes(locations, mode, recommended_mode = None, redundant_mode = None):
    if mode not in ["qualifier_metadata", "reference_metadata"]:
        error_message = "Not supported mode."
        raise Exception(error_message)

    if redundant_mode not in ["redundant", "non_redundant"]:
        error_message = "Not supported redundancy mode: ", redundant_mode
        raise Exception(error_message)

    datatypes_dict = {}
    datatypes_dict["datatypes"] = {}
    datatypes_dict["total_accumulated_datatypes"] = 0
    datatypes_dict["unique_datatypes"] = 0

    result_dict = {}
    result_dict["datatypes"] = {}
    result_dict["total_accumulated_datatypes"] = 0
    result_dict["unique_datatypes"] = 0

    for location in locations:

        if recommended_mode:
            tmp_string = "/recommended"
        elif recommended_mode is not None:
            tmp_string = "/non_recommended"
        else:
            tmp_string = "/all"

        path_to_datatypes_stat_information_timeframe = \
            "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" + redundant_mode + "/" + mode \
            + tmp_string + "/accumulated_datatypes/accumulated_datatypes.json"


        with open(path_to_datatypes_stat_information_timeframe, "r") as timeframe_data:
            timeframe_dict = json.load(timeframe_data)

            datatypes_dict["total_accumulated_datatypes"] += timeframe_dict["total_accumulated_datatypes"]

            for datatype in timeframe_dict["datatypes"]:

                if datatype in datatypes_dict["datatypes"]:
                    datatypes_dict["datatypes"][datatype] += timeframe_dict["datatypes"][datatype]
                else:
                    datatypes_dict["datatypes"][datatype] = timeframe_dict["datatypes"][datatype]
                    datatypes_dict["unique_datatypes"] += 1

        if recommended_mode:
            tmp_string = "/recommended"
        elif recommended_mode is not None:
            tmp_string = "/non_recommended"
        else:
            tmp_string = "/all"

    path_to_datatypes_stat_information_overall = \
        "data/statistical_information/query_research/" + redundant_mode + "/" + mode \
        + tmp_string + "/accumulated_datatypes/accumulated_datatypes.json"

    with open(path_to_datatypes_stat_information_overall, "w") as result_data:
        json.dump(datatypes_dict, result_data)

        result_data.close()


# only plot the non_redundant data
def summarize_additional_scenario_information_about_BIND(TIMEFRAMES):
    for metadata in ["reference_metadata", "qualifier_metadata", "rank_metadata"]:
        for redundant_mode in ["non_redundant"]:
            scenarios_dict = \
                {
                    "prop_one": 0,
                    "prop_two": 0,
                    "prop_three": 0,
                    "prop_four": 0,
                    "obj_one": 0,
                    "obj_two": 0,
                    "obj_three": 0,
                    "obj_four": 0,
                    "sub_one": 0,
                    "sub_two": 0,
                    "sub_three": 0,
                    "sub_four": 0,
                    "filter": 0,
                    "optional": 0,
                    "union": 0,
                    "prop_path": 0,
                    "bind": 0,
                    "blank_node": 0,
                    "minus": 0,
                    "subselect": 0,
                    "literal": 0,
                    "values": 0,
                    "service": 0,
                    "not_found_in_query": 0}

            result_dict = \
                {
                    "total_found_bound_variables_to_metadata": 0,
                    "variables_found_in_scenarios": scenarios_dict}
            for timeframe in TIMEFRAMES:

                path_to_information = "data/" + timeframe[:21] + "/" + timeframe[22:] + \
                                      "/" + metadata + "/scenarios/" + redundant_mode + \
                                      "/bind_statistical_information.json"
                if os.path.isfile(path_to_information):
                    with open(path_to_information, "r") as timeframe_data:
                        timeframe_dict = json.load(timeframe_data)

                        # summrize the timeframe data
                        result_dict["total_found_bound_variables_to_metadata"] += \
                            timeframe_dict["total_found_bound_variables_to_metadata"]
                        for scenario in scenarios_dict:
                            result_dict["variables_found_in_scenarios"][scenario] += \
                                timeframe_dict["variables_found_in_scenarios"][scenario]

                path_to_result = "data/statistical_information/query_research/" + redundant_mode + \
                                 "/" + metadata + "/scenarios/additional_layer/bind_statistical_information.json"
                with open(path_to_result, "w") as result_data:
                    json.dump(result_dict, result_data)


# only plot the non_redundant data
def summarize_additional_scenario_information_about_PROP_PATH(TIMEFRAMES):
    for metadata in ["reference_metadata", "qualifier_metadata", "rank_metadata"]:
        for redundant_mode in ["non_redundant"]:
            result_dict = \
                {
                    "total_found_operators": 0,
                    "found_operators_overall": {},
                    "found_operators_per_datatype": {}}
            for timeframe in TIMEFRAMES:


                path_to_information = "data/" + timeframe[:21] + "/" + timeframe[22:] + \
                                      "/" + metadata + "/scenarios/" + redundant_mode + \
                                      "/prop_path_statistical_information.json"

                if os.path.isfile(path_to_information):
                    with open(path_to_information, "r") as timeframe_data:
                        timeframe_dict = json.load(timeframe_data)

                        # summarize the timeframe data
                        result_dict["total_found_operators"] += \
                            timeframe_dict["total_found_operators"]

                        for operator in timeframe_dict["found_operators_overall"]:
                            if operator in result_dict["found_operators_overall"]:

                                result_dict["found_operators_overall"][operator] += \
                                    timeframe_dict["found_operators_overall"][operator]
                            else:
                                result_dict["found_operators_overall"][operator] = \
                                    timeframe_dict["found_operators_overall"][operator]

                        for datatype in timeframe_dict["found_operators_per_datatype"]:
                            if datatype in result_dict["found_operators_per_datatype"]:

                                for operator in timeframe_dict["found_operators_per_datatype"][datatype]:
                                    if operator in result_dict["found_operators_per_datatype"][datatype]:
                                        result_dict["found_operators_per_datatype"][datatype][operator] += \
                                            timeframe_dict["found_operators_per_datatype"][datatype][operator]
                                    else:
                                        result_dict["found_operators_per_datatype"][datatype][operator] = \
                                            timeframe_dict["found_operators_per_datatype"][datatype][operator]
                            else:
                                result_dict["found_operators_per_datatype"][datatype] = \
                                    timeframe_dict["found_operators_per_datatype"][datatype]


                path_to_result = "data/statistical_information/query_research/" + redundant_mode + \
                                 "/" + metadata + "/scenarios/additional_layer/prop_path_statistical_information.json"
                with open(path_to_result, "w") as result_data:
                    json.dump(result_dict, result_data)


# only plot the non_redundant data
def summarize_additional_scenario_information_about_FILTER(TIMEFRAMES):
    for metadata in ["reference_metadata", "qualifier_metadata", "rank_metadata"]:
        for redundant_mode in ["non_redundant"]:
            scenarios_dict = \
                {
                    "prop_one": 0,
                    "prop_two": 0,
                    "prop_three": 0,
                    "prop_four": 0,
                    "obj_one": 0,
                    "obj_two": 0,
                    "obj_three": 0,
                    "obj_four": 0,
                    "sub_one": 0,
                    "sub_two": 0,
                    "sub_three": 0,
                    "sub_four": 0,
                    "filter": 0,
                    "optional": 0,
                    "union": 0,
                    "prop_path": 0,
                    "bind": 0,
                    "blank_node": 0,
                    "minus": 0,
                    "subselect": 0,
                    "literal": 0,
                    "values": 0,
                    "service": 0,
                    "not_found_in_patterns": 0}


            result_dict = \
                {
                    "total_found_metadata": 0,
                    "metadata_found_in_scenarios": scenarios_dict,
                    "metadata_per_datatype_found_in_scenarios": {},
                    "total_found_operators": 0,
                    "found_operators_overall": {},
                    "found_operators_per_datatype": {}}

            for timeframe in TIMEFRAMES:

                path_to_information = "data/" + timeframe[:21] + "/" + timeframe[22:] + \
                                      "/" + metadata + "/scenarios/" + redundant_mode + \
                                      "/filter_statistical_information.json"

                if os.path.isfile(path_to_information):
                    with open(path_to_information, "r") as timeframe_data:
                        timeframe_dict = json.load(timeframe_data)

                        # summarize the timeframe data
                        result_dict["total_found_operators"] += \
                            timeframe_dict["total_found_operators"]
                        result_dict["total_found_metadata"] += \
                            timeframe_dict["total_found_metadata"]

                        for operator in timeframe_dict["found_operators_overall"]:
                            if operator in result_dict["found_operators_overall"]:

                                result_dict["found_operators_overall"][operator] += \
                                    timeframe_dict["found_operators_overall"][operator]
                            else:
                                result_dict["found_operators_overall"][operator] = \
                                    timeframe_dict["found_operators_overall"][operator]

                        for datatype in timeframe_dict["found_operators_per_datatype"]:
                            if datatype in result_dict["found_operators_per_datatype"]:

                                for operator in timeframe_dict["found_operators_per_datatype"][datatype]:
                                    if operator in result_dict["found_operators_per_datatype"][datatype]:
                                        result_dict["found_operators_per_datatype"][datatype][operator] += \
                                            timeframe_dict["found_operators_per_datatype"][datatype][operator]
                                    else:
                                        result_dict["found_operators_per_datatype"][datatype][operator] = \
                                            timeframe_dict["found_operators_per_datatype"][datatype][operator]
                            else:
                                result_dict["found_operators_per_datatype"][datatype] = \
                                    timeframe_dict["found_operators_per_datatype"][datatype]


                        for scenario in timeframe_dict["metadata_found_in_scenarios"]:
                            if scenario in result_dict["metadata_found_in_scenarios"]:

                                result_dict["metadata_found_in_scenarios"][scenario] += \
                                    timeframe_dict["metadata_found_in_scenarios"][scenario]
                            else:
                                result_dict["metadata_found_in_scenarios"][scenario] = \
                                    timeframe_dict["metadata_found_in_scenarios"][scenario]

                        for datatype in timeframe_dict["metadata_per_datatype_found_in_scenarios"]:
                            if datatype in result_dict["metadata_per_datatype_found_in_scenarios"]:

                                for scenario in timeframe_dict["metadata_per_datatype_found_in_scenarios"][datatype]:
                                    result_dict["metadata_per_datatype_found_in_scenarios"][datatype][scenario] += \
                                        timeframe_dict["metadata_per_datatype_found_in_scenarios"][datatype][scenario]
                            else:
                                result_dict["metadata_per_datatype_found_in_scenarios"][datatype] = \
                                    timeframe_dict["metadata_per_datatype_found_in_scenarios"][datatype]



                path_to_result = "data/statistical_information/query_research/" + redundant_mode + \
                                 "/" + metadata + "/scenarios/additional_layer/filter_statistical_information.json"
                with open(path_to_result, "w") as result_data:
                    json.dump(result_dict, result_data)


# only plot the non_redundant data
def summarize_additional_scenario_information_about_UNION(TIMEFRAMES):
    for metadata in ["reference_metadata", "qualifier_metadata", "rank_metadata"]:
        for redundant_mode in ["non_redundant"]:
            scenarios_dict = \
                {
                    "used_in_SELECT": 0,
                    "prop_one": 0,
                    "prop_two": 0,
                    "prop_three": 0,
                    "prop_four": 0,
                    "obj_one": 0,
                    "obj_two": 0,
                    "obj_three": 0,
                    "obj_four": 0,
                    "sub_one": 0,
                    "sub_two": 0,
                    "sub_three": 0,
                    "sub_four": 0,
                    "filter": 0,
                    "optional": 0,
                    "union": 0,
                    "prop_path": 0,
                    "bind": 0,
                    "blank_node": 0,
                    "minus": 0,
                    "subselect": 0,
                    "literal": 0,
                    "values": 0,
                    "service": 0,
                    "not_found_in_patterns": 0}

            result_dict = \
                {
                    "total_found_metadata": 0,
                    "metadata_found_in_scenarios": scenarios_dict,
                    "scenarios_found_in_second_level_subselect": scenarios_dict.copy(),
                    "metadata_per_datatype_found_in_scenarios": {},
                    "scenarios_per_datatype_found_in_second_level_subselect": {}
                }
            for timeframe in TIMEFRAMES:


                path_to_information = "data/" + timeframe[:21] + "/" + timeframe[22:] + \
                                      "/" + metadata + "/scenarios/" + redundant_mode + \
                                      "/union_statistical_information.json"

                if os.path.isfile(path_to_information):
                    with open(path_to_information, "r") as timeframe_data:
                        timeframe_dict = json.load(timeframe_data)

                        # summarize the timeframe data
                        result_dict["total_found_metadata"] += \
                            timeframe_dict["total_found_metadata"]

                        for scenario in timeframe_dict["metadata_found_in_scenarios"]:
                            if scenario in result_dict["metadata_found_in_scenarios"]:

                                result_dict["metadata_found_in_scenarios"][scenario] += \
                                    timeframe_dict["metadata_found_in_scenarios"][scenario]
                            else:
                                result_dict["metadata_found_in_scenarios"][scenario] = \
                                    timeframe_dict["metadata_found_in_scenarios"][scenario]

                        for datatype in timeframe_dict["metadata_per_datatype_found_in_scenarios"]:
                            if datatype in result_dict["metadata_per_datatype_found_in_scenarios"]:

                                for scenario in timeframe_dict["metadata_per_datatype_found_in_scenarios"][datatype]:
                                    result_dict["metadata_per_datatype_found_in_scenarios"][datatype][scenario] += \
                                        timeframe_dict["metadata_per_datatype_found_in_scenarios"][datatype][scenario]
                            else:
                                result_dict["metadata_per_datatype_found_in_scenarios"][datatype] = \
                                    timeframe_dict["metadata_per_datatype_found_in_scenarios"][datatype]



                        for scenario in timeframe_dict["scenarios_found_in_second_level_subselect"]:
                            if scenario in result_dict["scenarios_found_in_second_level_subselect"]:

                                result_dict["scenarios_found_in_second_level_subselect"][scenario] += \
                                    timeframe_dict["scenarios_found_in_second_level_subselect"][scenario]
                            else:
                                result_dict["scenarios_found_in_second_level_subselect"][scenario] = \
                                    timeframe_dict["scenarios_found_in_second_level_subselect"][scenario]

                        for datatype in timeframe_dict["scenarios_per_datatype_found_in_second_level_subselect"]:
                            if datatype in result_dict["scenarios_per_datatype_found_in_second_level_subselect"]:

                                for scenario in timeframe_dict["scenarios_per_datatype_found_in_second_level_subselect"][
                                    datatype]:
                                    result_dict["scenarios_per_datatype_found_in_second_level_subselect"][datatype][
                                        scenario] += \
                                        timeframe_dict["scenarios_per_datatype_found_in_second_level_subselect"][datatype][
                                            scenario]
                            else:
                                result_dict["scenarios_per_datatype_found_in_second_level_subselect"][datatype] = \
                                    timeframe_dict["scenarios_per_datatype_found_in_second_level_subselect"][datatype]

                path_to_result = "data/statistical_information/query_research/" + redundant_mode + \
                                 "/" + metadata + "/scenarios/additional_layer/union_statistical_information.json"
                with open(path_to_result, "w") as result_data:
                    json.dump(result_dict, result_data)


# only plot the non_redundant data
def summarize_additional_scenario_information_about_SUBSELECT(TIMEFRAMES):
    for metadata in ["reference_metadata", "qualifier_metadata", "rank_metadata"]:
        for redundant_mode in ["non_redundant"]:
            scenarios_dict = \
                {
                    "used_in_SELECT": 0,
                    "prop_one": 0,
                    "prop_two": 0,
                    "prop_three": 0,
                    "prop_four": 0,
                    "obj_one": 0,
                    "obj_two": 0,
                    "obj_three": 0,
                    "obj_four": 0,
                    "sub_one": 0,
                    "sub_two": 0,
                    "sub_three": 0,
                    "sub_four": 0,
                    "filter": 0,
                    "optional": 0,
                    "union": 0,
                    "prop_path": 0,
                    "bind": 0,
                    "blank_node": 0,
                    "minus": 0,
                    "subselect": 0,
                    "literal": 0,
                    "values": 0,
                    "service": 0,
                    "not_found_in_patterns": 0}


            result_dict = \
                {
                    "total_found_metadata": 0,
                    "metadata_found_in_scenarios": scenarios_dict,
                    "scenarios_found_in_second_level_union": scenarios_dict.copy(),
                    "metadata_per_datatype_found_in_scenarios": {},
                    "scenarios_per_datatype_found_in_second_level_union": {}
                }
        for timeframe in TIMEFRAMES:


                path_to_information = "data/" + timeframe[:21] + "/" + timeframe[22:] + \
                                      "/" + metadata + "/scenarios/" + redundant_mode + \
                                      "/subselect_statistical_information.json"

                if os.path.isfile(path_to_information):
                    with open(path_to_information, "r") as timeframe_data:
                        timeframe_dict = json.load(timeframe_data)

                        # summarize the timeframe data
                        result_dict["total_found_metadata"] += \
                            timeframe_dict["total_found_metadata"]

                        for scenario in timeframe_dict["metadata_found_in_scenarios"]:
                            if scenario in result_dict["metadata_found_in_scenarios"]:

                                result_dict["metadata_found_in_scenarios"][scenario] += \
                                    timeframe_dict["metadata_found_in_scenarios"][scenario]
                            else:
                                result_dict["metadata_found_in_scenarios"][scenario] = \
                                    timeframe_dict["metadata_found_in_scenarios"][scenario]

                        for datatype in timeframe_dict["metadata_per_datatype_found_in_scenarios"]:
                            if datatype in result_dict["metadata_per_datatype_found_in_scenarios"]:

                                for scenario in timeframe_dict["metadata_per_datatype_found_in_scenarios"][datatype]:
                                    result_dict["metadata_per_datatype_found_in_scenarios"][datatype][scenario] += \
                                        timeframe_dict["metadata_per_datatype_found_in_scenarios"][datatype][scenario]
                            else:
                                result_dict["metadata_per_datatype_found_in_scenarios"][datatype] = \
                                    timeframe_dict["metadata_per_datatype_found_in_scenarios"][datatype]



                        for scenario in timeframe_dict["scenarios_found_in_second_level_union"]:
                            if scenario in result_dict["scenarios_found_in_second_level_union"]:

                                result_dict["scenarios_found_in_second_level_union"][scenario] += \
                                    timeframe_dict["scenarios_found_in_second_level_union"][scenario]
                            else:
                                result_dict["scenarios_found_in_second_level_union"][scenario] = \
                                    timeframe_dict["scenarios_found_in_second_level_union"][scenario]

                        for datatype in timeframe_dict["scenarios_per_datatype_found_in_second_level_union"]:
                            if datatype in result_dict["scenarios_per_datatype_found_in_second_level_union"]:

                                for scenario in timeframe_dict["scenarios_per_datatype_found_in_second_level_union"][
                                    datatype]:
                                    result_dict["scenarios_per_datatype_found_in_second_level_union"][datatype][
                                        scenario] += \
                                        timeframe_dict["scenarios_per_datatype_found_in_second_level_union"][datatype][
                                            scenario]
                            else:
                                result_dict["scenarios_per_datatype_found_in_second_level_union"][datatype] = \
                                    timeframe_dict["scenarios_per_datatype_found_in_second_level_union"][datatype]

                path_to_result = "data/statistical_information/query_research/" + redundant_mode + \
                                 "/" + metadata + "/scenarios/additional_layer/subselect_statistical_information.json"
                with open(path_to_result, "w") as result_data:
                    json.dump(result_dict, result_data)


# only plot the non_redundant data
def summarize_additional_scenario_information_about_MINUS(TIMEFRAMES):
    for metadata in ["reference_metadata", "qualifier_metadata", "rank_metadata"]:
        for redundant_mode in ["non_redundant"]:
            scenarios_dict = \
                {
                    "prop_one": 0,
                    "prop_two": 0,
                    "prop_three": 0,
                    "prop_four": 0,
                    "obj_one": 0,
                    "obj_two": 0,
                    "obj_three": 0,
                    "obj_four": 0,
                    "sub_one": 0,
                    "sub_two": 0,
                    "sub_three": 0,
                    "sub_four": 0,
                    "filter": 0,
                    "optional": 0,
                    "union": 0,
                    "prop_path": 0,
                    "bind": 0,
                    "blank_node": 0,
                    "minus": 0,
                    "subselect": 0,
                    "literal": 0,
                    "values": 0,
                    "service": 0,
                    "not_found_in_patterns": 0}

            result_dict = \
                {
                    "total_found_metadata": 0,
                    "metadata_found_in_scenarios": scenarios_dict,
                    "metadata_per_datatype_found_in_scenarios": {}}
            for timeframe in TIMEFRAMES:


                path_to_information = "data/" + timeframe[:21] + "/" + timeframe[22:] + \
                                      "/" + metadata + "/scenarios/" + redundant_mode + \
                                      "/minus_statistical_information.json"

                if os.path.isfile(path_to_information):
                    with open(path_to_information, "r") as timeframe_data:
                        timeframe_dict = json.load(timeframe_data)

                        # summarize the timeframe data
                        result_dict["total_found_metadata"] += \
                            timeframe_dict["total_found_metadata"]

                        for scenario in timeframe_dict["metadata_found_in_scenarios"]:
                            if scenario in result_dict["metadata_found_in_scenarios"]:

                                result_dict["metadata_found_in_scenarios"][scenario] += \
                                    timeframe_dict["metadata_found_in_scenarios"][scenario]
                            else:
                                result_dict["metadata_found_in_scenarios"][scenario] = \
                                    timeframe_dict["metadata_found_in_scenarios"][scenario]

                        for datatype in timeframe_dict["metadata_per_datatype_found_in_scenarios"]:
                            if datatype in result_dict["metadata_per_datatype_found_in_scenarios"]:

                                for scenario in timeframe_dict["metadata_per_datatype_found_in_scenarios"][datatype]:
                                    result_dict["metadata_per_datatype_found_in_scenarios"][datatype][scenario] += \
                                        timeframe_dict["metadata_per_datatype_found_in_scenarios"][datatype][scenario]
                            else:
                                result_dict["metadata_per_datatype_found_in_scenarios"][datatype] = \
                                    timeframe_dict["metadata_per_datatype_found_in_scenarios"][datatype]


                path_to_result = "data/statistical_information/query_research/" + redundant_mode + \
                                 "/" + metadata + "/scenarios/additional_layer/minus_statistical_information.json"
                with open(path_to_result, "w") as result_data:
                    json.dump(result_dict, result_data)


# only plot the non_redundant data
def summarize_additional_scenario_information_about_OPTIONAL(TIMEFRAMES):
    for metadata in ["reference_metadata", "qualifier_metadata", "rank_metadata"]:
        for redundant_mode in ["non_redundant"]:
            scenarios_dict = \
                {
                    "prop_one": 0,
                    "prop_two": 0,
                    "prop_three": 0,
                    "prop_four": 0,
                    "obj_one": 0,
                    "obj_two": 0,
                    "obj_three": 0,
                    "obj_four": 0,
                    "sub_one": 0,
                    "sub_two": 0,
                    "sub_three": 0,
                    "sub_four": 0,
                    "filter": 0,
                    "optional": 0,
                    "union": 0,
                    "prop_path": 0,
                    "bind": 0,
                    "blank_node": 0,
                    "minus": 0,
                    "subselect": 0,
                    "literal": 0,
                    "values": 0,
                    "service": 0,
                    "not_found_in_patterns": 0}

            result_dict = \
                {
                    "total_found_metadata": 0,
                    "metadata_found_in_scenarios": scenarios_dict,
                    "metadata_per_datatype_found_in_scenarios": {},
                    "in_found_prop_path_total_found_operators": 0,
                    "in_found_prop_path_found_operators_overall": {},
                    "in_found_prop_path_found_operators_per_datatype": {}
                }

            for timeframe in TIMEFRAMES:


                path_to_information = "data/" + timeframe[:21] + "/" + timeframe[22:] + \
                                      "/" + metadata + "/scenarios/" + redundant_mode + \
                                      "/optional_statistical_information.json"

                if os.path.isfile(path_to_information):
                    with open(path_to_information, "r") as timeframe_data:
                        timeframe_dict = json.load(timeframe_data)

                        # summarize the timeframe data
                        result_dict["total_found_metadata"] += \
                            timeframe_dict["total_found_metadata"]

                        for scenario in timeframe_dict["metadata_found_in_scenarios"]:
                            if scenario in result_dict["metadata_found_in_scenarios"]:

                                result_dict["metadata_found_in_scenarios"][scenario] += \
                                    timeframe_dict["metadata_found_in_scenarios"][scenario]
                            else:
                                result_dict["metadata_found_in_scenarios"][scenario] = \
                                    timeframe_dict["metadata_found_in_scenarios"][scenario]

                        for datatype in timeframe_dict["metadata_per_datatype_found_in_scenarios"]:
                            if datatype in result_dict["metadata_per_datatype_found_in_scenarios"]:

                                for scenario in timeframe_dict["metadata_per_datatype_found_in_scenarios"][datatype]:
                                    result_dict["metadata_per_datatype_found_in_scenarios"][datatype][scenario] += \
                                        timeframe_dict["metadata_per_datatype_found_in_scenarios"][datatype][scenario]
                            else:
                                result_dict["metadata_per_datatype_found_in_scenarios"][datatype] = \
                                    timeframe_dict["metadata_per_datatype_found_in_scenarios"][datatype]

                        result_dict["in_found_prop_path_total_found_operators"] += \
                            timeframe_dict["in_found_prop_path_total_found_operators"]

                        for operator in timeframe_dict["in_found_prop_path_found_operators_overall"]:
                            if operator in result_dict["in_found_prop_path_found_operators_overall"]:

                                result_dict["in_found_prop_path_found_operators_overall"][operator] += \
                                    timeframe_dict["in_found_prop_path_found_operators_overall"][operator]
                            else:
                                result_dict["in_found_prop_path_found_operators_overall"][operator] = \
                                    timeframe_dict["in_found_prop_path_found_operators_overall"][operator]

                        for datatype in timeframe_dict["in_found_prop_path_found_operators_per_datatype"]:
                            if datatype in result_dict["in_found_prop_path_found_operators_per_datatype"]:

                                for operator in timeframe_dict["in_found_prop_path_found_operators_per_datatype"][datatype]:
                                    if operator in result_dict["in_found_prop_path_found_operators_per_datatype"][datatype]:
                                        result_dict["in_found_prop_path_found_operators_per_datatype"][datatype][operator] += \
                                            timeframe_dict["in_found_prop_path_found_operators_per_datatype"][datatype][operator]
                                    else:
                                        result_dict["in_found_prop_path_found_operators_per_datatype"][datatype][operator] = \
                                            timeframe_dict["in_found_prop_path_found_operators_per_datatype"][datatype][operator]
                            else:
                                result_dict["in_found_prop_path_found_operators_per_datatype"][datatype] = \
                                    timeframe_dict["in_found_prop_path_found_operators_per_datatype"][datatype]



                path_to_result = "data/statistical_information/query_research/" + redundant_mode + \
                                 "/" + metadata + "/scenarios/additional_layer/optional_statistical_information.json"
                with open(path_to_result, "w") as result_data:
                    json.dump(result_dict, result_data)

