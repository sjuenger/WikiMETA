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
            "looking_for" : looking_for,
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
            "union" : 0,
            "prop_path" : 0,
            "other": 0}

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

                    if scenario_one_detection.is_scenario_one(json_object, looking_for):
                        dict_looking_for["one"] += 1
                        # copy the corresponding sparql file (to the JSON file) to a specific folder for scenarios
                        # .. used for debugging and review of the results
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/one")

                    if scenario_two_detection.is_scenario_two(json_object, looking_for):
                        dict_looking_for["two"] += 1
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/two")
                    if scenario_three_detection.is_scenario_three(json_object, looking_for):
                        dict_looking_for["three"] += 1
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/three")
                    if scenario_four_detection.is_scenario_four(json_object, looking_for):
                        dict_looking_for["four"] += 1
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/four")

                    if scenario_five_detection.is_scenario_five(json_object, looking_for):
                        dict_looking_for["five"] += 1
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/five")
                    if scenario_six_detection.is_scenario_six(json_object, looking_for):
                        dict_looking_for["six"] += 1
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/six")
                    if scenario_seven_detection.is_scenario_seven(json_object, looking_for):
                        dict_looking_for["seven"] += 1
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/seven")
                    if scenario_eight_detection.is_scenario_eight(json_object, looking_for):
                        dict_looking_for["eight"] += 1
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/eight")

                    if scenario_nine_detection.is_scenario_nine(json_object, looking_for):
                        dict_looking_for["nine"] += 1
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/nine")
                    if scenario_ten_detection.is_scenario_ten(json_object, looking_for):
                        dict_looking_for["ten"] += 1
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/ten")
                    if scenario_eleven_detection.is_scenario_eleven(json_object, looking_for):
                        dict_looking_for["eleven"] += 1
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/eleven")
                    if scenario_twelve_detection.is_scenario_twelve(json_object, looking_for):
                        dict_looking_for["twelve"] += 1
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/twelve")

                    if scenario_filter_detection.is_scenario_filter(json_object, looking_for):
                        dict_looking_for["filter"] += 1
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/filter")
                    if scenario_optional_detection.is_scenario_optional(json_object, looking_for):
                        dict_looking_for["optional"] += 1
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/optional")
                    if scenario_union_detection.is_scenario_union(json_object, looking_for):
                        dict_looking_for["union"] += 1
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/union")
                    if scenario_prop_path_detection.is_scenario_prop_path(json_object, looking_for):
                        dict_looking_for["prop_path"] += 1
                        shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/prop_path")

                    # check  if non scenario was applied
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
        return ["http://www.wikidata.org/reference", "http://www.wikidata.org/prop/reference",
                "http://www.w3.org/ns/prov#wasDerivedFrom"]
    elif data_type == "reference_metadata/derived_+_reference_node":
        return ["http://www.wikidata.org/reference", "http://www.w3.org/ns/prov#wasDerivedFrom"]
    elif data_type == "reference_metadata/derived_+_reference_property":
        return ["http://www.wikidata.org/prop/reference", "http://www.w3.org/ns/prov#wasDerivedFrom"]
    elif data_type == "reference_metadata/only_derived":
        return ["http://www.w3.org/ns/prov#wasDerivedFrom"]
    elif data_type == "reference_metadata/only_reference_node":
        return ["http://www.wikidata.org/reference"]
    elif data_type == "reference_metadata/only_reference_property":
        return ["http://www.wikidata.org/prop/reference"]
    elif data_type == "reference_metadata/reference_node_+_reference_property":
        return ["http://www.wikidata.org/prop/reference", "http://www.wikidata.org/reference"]

