import json
import glob
import os
import shutil

"""{
# scenario 5:
# BIND( ...

# Property Path
# Union ...
# Having

# scenario X for DESCRIBE, CONSTRUCT, ...?

# Others in others
}"""

import query_research.scenarios.scenario_1_detection as scenario_one_detection
import query_research.scenarios.scenario_2_detection as scenario_two_detection
import query_research.scenarios.scenario_3_detection as scenario_three_detection
import query_research.scenarios.scenario_4_detection as scenario_four_detection

import query_research.scenarios.scenario_5_detection as scenario_five_detection
import query_research.scenarios.scenario_6_detection as scenario_six_detection
import query_research.scenarios.scenario_7_detection as scenario_seven_detection
import query_research.scenarios.scenario_8_detection as scenario_eight_detection

import query_research.scenarios.scenario_9_detection as scenario_nine_detection
import query_research.scenarios.scenario_10_detection as scenario_ten_detection
import query_research.scenarios.scenario_11_detection as scenario_eleven_detection
import query_research.scenarios.scenario_12_detection as scenario_twelve_detection

import query_research.scenarios.scenario_filter_detection as scenario_filter_detection
import query_research.scenarios.scenario_optional_detection as scenario_optional_detection
import query_research.scenarios.scenario_union_detection as scenario_union_detection
import query_research.scenarios.scenario_prop_path_detection as scenario_prop_path_detection
import query_research.scenarios.scenario_group_detection as scenario_group_detection
import query_research.scenarios.scenario_bind_detection as scenario_bind_detection
import query_research.scenarios.scenario_blank_node_detection as scenario_blank_node_detection
import query_research.scenarios.scenario_minus_detection as scenario_minus_detection
import query_research.scenarios.scenario_subselect_detection as scenario_subselect_detection
import query_research.scenarios.scenario_ref_value_detection as scenario_ref_value_detection
import query_research.scenarios.scenario_literal_detection as scenario_literal_detection

def detect_scenarios(location, data_type):
    # Retrieve all files, ending with .json
    files_json = glob.glob("data/" + location[:21] + "/" +
                             location[22:] + "/" + data_type + "/*.json")
    # get the path to the folder, where all scenarios are saved
    path_to_scenarios = "data/" + location[:21] + "/" + location[22:] + "/" + \
                        data_type.split('/')[0] + "/scenarios"
    # get the path to the folder, where the json file about the gathered statistical information
    # .. is stored
    path_to_stat_information = "data/" + location[:21] + "/" + location[22:] + "/" + \
                        data_type.split('/')[0] + "/statistical_information"


    total_SELECT_queries = 0
    total_DESCRIBE_queries = 0
    total_CONSTRUCT_queries = 0
    total_ASK_queries = 0

    # a scenario fora non-recognized scenario

    # auch BIND als scenario
    # property path als scenario

    # to check for the type of the SPARQL query (SELECT, DESCRIBE, ASK, CONSTRUCT)
    for query_file in files_json:
        if os.path.isfile(query_file.title().lower()):
            with open(query_file, "rt") as json_data:
                json_object = json.load(json_data)

                if json_object["queryType"] == "SELECT":
                    total_SELECT_queries += 1
                elif json_object["queryType"] == "DESCRIBE":
                    total_DESCRIBE_queries += 1
                elif json_object["queryType"] == "ASK":
                    total_ASK_queries += 1
                elif json_object["queryType"] == "CONSTRUCT":
                    total_CONSTRUCT_queries += 1


    # to check for the scenarios

    array_looking_for = get_mode(data_type)

    dict_overview_looking_for = {"list_per_search": []}

    for looking_for in array_looking_for:

        # create a scenario per "looking for" , e.g. "wasDerivedFrom"
        dict_looking_for = {
            "looking_for": looking_for,
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
            "other": 0}
        # TODO: Ad "total" occurences of a "looking for"

        for query_file in files_json:
            if os.path.isfile(query_file.title().lower()):
                with open(query_file, "rt") as json_data:
                    json_object = json.load(json_data)

                    # the path to the sparql text file (corresponding to the json object
                    # to later be able to copy the sparql text file to a specific directors (for debugging)
                    # Data/2017-06-12_2017-07-09/Organic/Reference_Metadata/Derived_+_Reference_Property/182150 2017-07-07 19:06:30.json
                    # -->
                    # Data/2017-06-12_2017-07-09/Organic/Reference_Metadata/Derived_+_Reference_Property/182150 2017-07-07 19:06:30.sparql
                    path_to_sparql_text_file = query_file[:-4]+"sparql"

                    # to later check, if something changed in the list
                    # -> to detect, if a scenario did apply
                    tmp_dict = dict_looking_for.copy()

                    # scenario one
                    occurrences_scenario_one = scenario_one_detection.scenario_one_occurrences(json_object, looking_for)
                    dict_looking_for["one"] += occurrences_scenario_one
                    if occurrences_scenario_one > 0:
                        # copy the corresponding sparql file (to the JSON file) to a specific folder for scenarios
                        # .. used for debugging and review of the results
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/one")

                    # scenario two
                    occurrences_scenario_two = scenario_two_detection.scenario_two_occurrences(json_object, looking_for)
                    dict_looking_for["two"] += occurrences_scenario_two
                    if occurrences_scenario_two > 0:
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/two")

                    # scenario three
                    occurrences_scenario_three = \
                        scenario_three_detection.scenario_three_occurrences(json_object, looking_for)
                    dict_looking_for["three"] += occurrences_scenario_three
                    if occurrences_scenario_three > 0:
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/three")

                    # scenario four
                    occurrences_scenario_four = \
                        scenario_four_detection.scenario_four_occurrences(json_object, looking_for)
                    dict_looking_for["four"] += occurrences_scenario_four
                    if occurrences_scenario_four > 0:
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/four")

                    # scenario five
                    occurrences_scenario_five = \
                        scenario_five_detection.scenario_five_occurrences(json_object, looking_for)
                    dict_looking_for["five"] += occurrences_scenario_five
                    if occurrences_scenario_five > 0:
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/five")

                    # scenario six
                    occurrences_scenario_six = scenario_six_detection.scenario_six_occurrences(json_object, looking_for)
                    dict_looking_for["six"] += occurrences_scenario_six
                    if occurrences_scenario_six > 0:
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/six")

                    # scenario seven
                    occurrences_scenario_seven = \
                        scenario_seven_detection.scenario_seven_occurrences(json_object, looking_for)
                    dict_looking_for["seven"] += occurrences_scenario_seven
                    if occurrences_scenario_seven > 0:
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/seven")

                    # scenario eight
                    occurrences_scenario_eight = \
                        scenario_eight_detection.scenario_eight_occurrences(json_object, looking_for)
                    dict_looking_for["eight"] += occurrences_scenario_eight
                    if occurrences_scenario_eight > 0:
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/eight")

                    # scenario nine
                    occurrences_scenario_nine = \
                        scenario_nine_detection.scenario_nine_occurrences(json_object, looking_for)
                    dict_looking_for["nine"] += occurrences_scenario_nine
                    if occurrences_scenario_nine > 0:
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/nine")

                    # scenario ten
                    occurrences_scenario_ten = scenario_ten_detection.scenario_ten_occurrences(json_object, looking_for)
                    dict_looking_for["ten"] += occurrences_scenario_ten
                    if occurrences_scenario_ten > 0:
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/ten")

                    # scenario eleven
                    occurrences_scenario_eleven = \
                        scenario_eleven_detection.scenario_eleven_occurrences(json_object, looking_for)
                    dict_looking_for["eleven"] += occurrences_scenario_eleven
                    if occurrences_scenario_eleven > 0:
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/eleven")

                    # scenario twelve
                    occurrences_scenario_twelve = \
                        scenario_twelve_detection.scenario_twelve_occurrences(json_object, looking_for)
                    dict_looking_for["twelve"] += occurrences_scenario_twelve
                    if occurrences_scenario_twelve > 0:
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/twelve")

                    # scenario filter
                    occurrences_scenario_filter = \
                        scenario_filter_detection.scenario_filter_occurrences(json_object, looking_for)
                    dict_looking_for["filter"] += occurrences_scenario_filter
                    if occurrences_scenario_filter > 0:
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/filter")

                    # scenario optional
                    occurrences_scenario_optional = \
                        scenario_optional_detection.scenario_optional_occurrences(json_object, looking_for)
                    dict_looking_for["optional"] += occurrences_scenario_optional
                    if occurrences_scenario_optional > 0:
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/optional")

                    # scenario union
                    occurrences_scenario_union = \
                        scenario_union_detection.scenario_union_occurrences(json_object, looking_for)
                    dict_looking_for["union"] += occurrences_scenario_union
                    if occurrences_scenario_union > 0:
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/union")

                    # scenario property path
                    occurrences_scenario_prop_path = \
                        scenario_prop_path_detection.scenario_prop_path_occurrences(json_object, looking_for)
                    dict_looking_for["prop_path"] += occurrences_scenario_prop_path
                    if occurrences_scenario_prop_path > 0:
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/prop_path")

                    # scenario group
                    occurrences_scenario_group = \
                        scenario_group_detection.scenario_group_occurrences(json_object, looking_for)
                    dict_looking_for["group"] += occurrences_scenario_group
                    if occurrences_scenario_group > 0:
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/group")

                    # scenario bind
                    occurrences_scenario_bind = \
                        scenario_bind_detection.scenario_bind_occurrences(json_object, looking_for)
                    dict_looking_for["bind"] += occurrences_scenario_bind
                    if occurrences_scenario_bind > 0:
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/bind")

                    # scenario blank node
                    occurrences_scenario_blank_node = \
                        scenario_blank_node_detection.scenario_blank_node_occurrences(json_object, looking_for)
                    dict_looking_for["blank_node"] += occurrences_scenario_blank_node
                    if occurrences_scenario_blank_node > 0:
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/blank_node")

                    # scenario minus
                    occurrences_scenario_minus = \
                        scenario_minus_detection.scenario_minus_occurrences(json_object, looking_for)
                    dict_looking_for["minus"] += occurrences_scenario_minus
                    if occurrences_scenario_minus > 0:
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/minus")

                    # scenario subselect
                    occurrences_scenario_subselect = \
                        scenario_subselect_detection.scenario_subselect_occurrences(json_object, looking_for)
                    dict_looking_for["subselect"] += occurrences_scenario_subselect
                    if occurrences_scenario_subselect > 0:
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/subselect")

                    # scenario ref value
                    occurrences_scenario_ref_value = \
                        scenario_ref_value_detection.scenario_ref_value_occurrences(json_object, looking_for)
                    dict_looking_for["ref_value"] += occurrences_scenario_ref_value
                    if occurrences_scenario_ref_value > 0:
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/ref_value")

                    # scenario literal
                    occurrences_scenario_literal = \
                        scenario_literal_detection.scenario_literal_occurrences(json_object, looking_for)
                    dict_looking_for["literal"] += occurrences_scenario_literal
                    if occurrences_scenario_literal > 0:
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/literal")

                    # check  if no scenario did apply
                    if dict_looking_for == tmp_dict:
                        dict_looking_for["other"] += 1
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/other")
                        # with the "other" -> also copy the .json file
                        # -> so, it is a bit easier to develop new filters
                        shutil.copy(query_file, path_to_scenarios + "/other")


        # attach the dictionary for looking for to the dictionary for the whole data type
        dict_overview_looking_for["list_per_search"].append(dict_looking_for)


    scenario_dict = {
        "data_type": data_type,
        "total queries": files_json.__len__(),
        "SELECT_queries": total_SELECT_queries,
        "DESCRIBE_queries": total_DESCRIBE_queries,
        "CONSTRUCT_queries": total_CONSTRUCT_queries,
        "ASK_queries": total_ASK_queries,
        "found_scenarios": dict_overview_looking_for
    }


    # save the scneario_dict to a folder
    with open(path_to_stat_information + "/" + data_type.split('/')[1] , "wt") as information_data:
        json.dump(scenario_dict, information_data)

    # test the bind variables

    return


def get_mode(data_type):
    if data_type == "reference_metadata/all_three":
        return ["http://www.wikidata.org/reference/", "http://www.wikidata.org/prop/reference/P",
                "http://www.w3.org/ns/prov#wasDerivedFrom"]
    elif data_type == "reference_metadata/derived_+_reference_node":
        return ["http://www.wikidata.org/reference/", "http://www.w3.org/ns/prov#wasDerivedFrom"]
    elif data_type == "reference_metadata/derived_+_reference_property":
        return ["http://www.wikidata.org/prop/reference/P", "http://www.w3.org/ns/prov#wasDerivedFrom"]
    elif data_type == "reference_metadata/only_derived":
        return ["http://www.w3.org/ns/prov#wasDerivedFrom"]
    elif data_type == "reference_metadata/only_reference_node":
        return ["http://www.wikidata.org/reference/"]
    elif data_type == "reference_metadata/only_reference_property":
        return ["http://www.wikidata.org/prop/reference/P"]
    elif data_type == "reference_metadata/reference_node_+_reference_property":
        return ["http://www.wikidata.org/prop/reference/P", "http://www.wikidata.org/reference/"]

