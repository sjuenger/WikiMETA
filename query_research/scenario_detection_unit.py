import json
import glob
import os

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

def detect_scenarios(location, data_type):
    # Retrieve all files, ending with .json
    files_sparql = glob.glob("data/" + location[:21] + "/" +
                             location[22:] + "/" + data_type + "/*.json")

    print(".json files in total in this folder: ", files_sparql.__len__())

    total_SELECT_queries = 0
    total_DESCRIBE_queries = 0
    total_CONSTRUCT_queries = 0
    total_ASK_queries = 0

    # create a dictionary -> to count the different scenarios
    scenario_dict = {
    "one" : 0,\
    "two" : 0,\
    "three" : 0,\
    "four" : 0,\
    "five" : 0,\
    "six" : 0,\
    "seven" : 0,\
    "eight" : 0,\
    "nine" : 0,\
    "ten" : 0,\
    "eleven" : 0,\
    "twelve" : 0,\
    "filter" : 0,\
    "optional" : 0,\
    "others" : 0
    }
    # a scenario fora non-recognized scenario

    # auch BIND als scenario
    # property path als scenario


    array_looking_for = get_mode(data_type)


    i = 0

    for looking_for in array_looking_for:
        for query_file in files_sparql:
            if os.path.isfile(query_file.title().lower()):
                with open(query_file, "rt") as json_data:
                    json_object = json.load(json_data)

                    if json_object["queryType"] == "SELECT":
                        total_SELECT_queries += 1

                        # to later check, if something changed in the list
                        # -> to detect, if a scenario did apply
                        tmp_dict = scenario_dict

                        if scenario_one_detection.is_scenario_one(json_object, looking_for):
                            scenario_dict["one"] += 1
                        if scenario_two_detection.is_scenario_two(json_object, looking_for):
                            scenario_dict["two"] += 1
                        if scenario_three_detection.is_scenario_three(json_object, looking_for):
                            scenario_dict["three"] += 1
                        if scenario_four_detection.is_scenario_four(json_object, looking_for):
                            scenario_dict["four"] += 1

                        if scenario_five_detection.is_scenario_five(json_object, looking_for):
                            scenario_dict["five"] += 1
                        if scenario_six_detection.is_scenario_six(json_object, looking_for):
                            scenario_dict["six"] += 1
                        if scenario_seven_detection.is_scenario_seven(json_object, looking_for):
                            scenario_dict["seven"] += 1
                        if scenario_eight_detection.is_scenario_eight(json_object, looking_for):
                            scenario_dict["eight"] += 1

                        if scenario_nine_detection.is_scenario_nine(json_object, looking_for):
                            scenario_dict["nine"] += 1
                        if scenario_ten_detection.is_scenario_ten(json_object, looking_for):
                            scenario_dict["ten"] += 1
                        if scenario_eleven_detection.is_scenario_eleven(json_object, looking_for):
                            scenario_dict["eleven"] += 1
                        if scenario_twelve_detection.is_scenario_twelve(json_object, looking_for):
                            scenario_dict["twelve"] += 1

                        if scenario_filter_detection.is_scenario_filter(json_object, looking_for):
                            scenario_dict["filter"] += 1
                        if scenario_optional_detection.is_scenario_optional(json_object, looking_for):
                            scenario_dict["optional"] += 1

                        # check  if non scenario was applied
                        if scenario_dict == tmp_dict:
                            scenario_dict["others"] += 1


                        #print(query_file)

                    elif json_object["queryType"] == "DESCRIBE":
                        total_DESCRIBE_queries += 1
                    elif json_object["queryType"] == "ASK":
                        total_ASK_queries += 1
                    elif json_object["queryType"] == "CONSTRUCT":
                        total_CONSTRUCT_queries += 1

        print(data_type)
        print(looking_for)

        print("scenario one: ", scenario_dict["one"])
        print("scenario two: ", scenario_dict["two"])
        print("scenario three: ", scenario_dict["three"])
        print("scenario four: ", scenario_dict["four"])

        print("scenario five: ", scenario_dict["five"])
        print("scenario six: ", scenario_dict["six"])
        print("scenario seven: ", scenario_dict["seven"])
        print("scenario eight: ", scenario_dict["eight"])

        print("scenario nine: ", scenario_dict["nine"]) # not yet tested
        print("scenario ten: ", scenario_dict["ten"]) # not yet tested
        print("scenario eleven: ", scenario_dict["eleven"]) # not yet tested
        print("scenario twelve: ", scenario_dict["twelve"]) # not yet tested

        # not yet tested
        print("scenario filter: ", scenario_dict["filter"])
        print("scenario optional: ", scenario_dict["optional"])
        print("scenario others: ", scenario_dict["others"], "\n")

        # ! delete the test.json file !
        # test the bind variables
    print("\n")
    return


def get_mode(data_type):
    if data_type == "reference_metadata/all_three":
        return ["http://www.wikidata.org/reference", "http://www.wikidata.org/prop/reference",
                "http://www.w3.org/ns/prov#wasDerivedFrom"]
    elif data_type == "reference_metadata/derived_+_reference_node":
        return ["http://www.wikidata.org/reference", "http://www.w3.org/ns/prov#wasDerivedFrom"]
    elif data_type == "reference_metadata/derived_+_reference_property":
        return ["http://www.wikidata.org/prop/reference", "http://www.w3.org/ns/prov#wasDerivedFrom"]
    elif data_type == "reference_metadata/donly_derived":
        return ["http://www.w3.org/ns/prov#wasDerivedFrom"]
    elif data_type == "reference_metadata/only_reference_node":
        return ["http://www.wikidata.org/reference"]
    elif data_type == "reference_metadata/only_reference_property":
        return ["http://www.wikidata.org/prop/reference"]
    elif data_type == "reference_metadata/reference_node_+_reference_property":
        return ["http://www.wikidata.org/prop/reference", "http://www.wikidata.org/reference"]

