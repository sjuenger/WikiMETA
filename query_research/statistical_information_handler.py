import glob
import json

# the purpose of this module is to summarize the many different statistical informations at different stages
# .. in the /data folder to one for every 'hierarchy step'

# summarize the statistical information about the different "sub-metadata" e.g. 'derived_+_reference_property'
# .. to one .json file for the entire metadata
# .. e.g. for References, Qualifiers, Ranks
def summarize_statistical_information_about_scenarios(location, datatype_list, metadata):
    # struct for the resulting .json object

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
        "ref_value": 0,
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
        path_to_stat_information_subtypes = "data/" + location[:21] + "/" + location[22:] + "/" + \
                            datatype.split('/')[0] + "/statistical_information/" + datatype.split('/')[1]
        path_to_stat_information_metadata = "data/" + location[:21] + "/" + location[22:] +\
                             "/statistical_information/" + metadata + ".json"

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
                metadata_dict["found_scenarios"]["ref_value"] += \
                    elem["ref_value"]
                metadata_dict["found_scenarios"]["service"] += \
                    elem["service"]
                metadata_dict["found_scenarios"]["subselect"] = \
                    elem["subselect"]
                metadata_dict["found_scenarios"]["union"] = \
                    elem["union"]
                metadata_dict["found_scenarios"]["values"] = \
                    elem["values"]

    with open(path_to_stat_information_metadata, "w") as json_result:
        json.dump(metadata_dict, json_result)


# summarize the statistical information about the different timeframes
def summarize_statistical_information_about_metadata(location, datatype_list, timeframe):
    # struct for the resulting .json object

    dict_looking_for = {
        "looking_for": timeframe,
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
        "ref_value": 0,
        "literal": 0,
        "values": 0,
        "service": 0,
        "other": 0}

    metadata_dict = {
        "data_type": timeframe,
        "total_queries": 0,
        "SELECT_queries": 0,
        "DESCRIBE_queries": 0,
        "CONSTRUCT_queries": 0,
        "ASK_queries": 0,
        "found_scenarios": dict_looking_for
    }

    for datatype in datatype_list:
        # get the path to the folder, where the json file about the gathered statistical information
        # .. about the metadata is stored (on the current timeframe)

        path_to_stat_information_metadata = "data/" + location[:21] + "/" + location[22:] +\
                             "/statistical_information/" + datatype + ".json"
        path_to_stat_information_timeframe = "data/statistical_information/" + datatype + ".json"

        # extract the statistical information
        with open(path_to_stat_information_metadata, "r") as json_data:
            metadata_subtype_dict = json.load(json_data)

            # update the metadata_dict
            metadata_dict["total_queries"] += metadata_subtype_dict["total_queries"]
            metadata_dict["SELECT_queries"] += metadata_subtype_dict["SELECT_queries"]
            metadata_dict["DESCRIBE_queries"] += metadata_subtype_dict["DESCRIBE_queries"]
            metadata_dict["CONSTRUCT_queries"] += metadata_subtype_dict["CONSTRUCT_queries"]
            metadata_dict["ASK_queries"] += metadata_subtype_dict["ASK_queries"]

            for elem in metadata_subtype_dict["found_scenarios"]["list_per_search"]:
            elem = metadata_subtype_dict

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
                metadata_dict["found_scenarios"]["ref_value"] += \
                    elem["ref_value"]
                metadata_dict["found_scenarios"]["service"] += \
                    elem["service"]
                metadata_dict["found_scenarios"]["subselect"] = \
                    elem["subselect"]
                metadata_dict["found_scenarios"]["union"] = \
                    elem["union"]
                metadata_dict["found_scenarios"]["values"] = \
                    elem["values"]

    with open(path_to_stat_information_metadata, "w") as json_result:
        json.dump(metadata_dict, json_result)
