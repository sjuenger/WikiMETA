import json
import glob
import os

# constellation for "wasDerivedFrom"

# scenario 1:
# ?s prov:wasDerivedFrom ?o

# scenario 2:
# BOUND prov:wasDerivedFrom ?o

# scenario 3:
# ?s prov:wasDerivedFrom BOUND

# scenario 4:
# BOUND prov:wasDerivedFrom ?o

#OTHERS
"""{
# scenario 5:
# BIND( ...

# Property Path
# Union ...
# Having

# scenario X for DESCRIBE, CONSTRUCT, ...?

# Others in others
}"""

import query_research.scenarios.scenario_one_detection as scenario_one_detection
import query_research.scenarios.scenario_two_detection as scenario_two_detection
import query_research.scenarios.scenario_three_detection as scenario_three_detection
import query_research.scenarios.scenario_four_detection as scenario_four_detection

import query_research.scenarios.scenario_five_detection as scenario_five_detection
import query_research.scenarios.scenario_six_detection as scenario_six_detection
import query_research.scenarios.scenario_seven_detection as scenario_seven_detection
import query_research.scenarios.scenario_eight_detection as scenario_eight_detection

import query_research.scenarios.scenario_nine_detection as scenario_nine_detection
import query_research.scenarios.scenario_ten_detection as scenario_ten_detection
import query_research.scenarios.scenario_eleven_detection as scenario_eleven_detection
import query_research.scenarios.scenario_twelve_detection as scenario_twelve_detection

import query_research.scenarios.scenario_filter_detection as scenario_filter_detection

def detect_scenarios(location, data_type):
    # Retrieve all files, ending with .json
    files_sparql = glob.glob("data/" + location[:21] + "/" +
                             location[22:] + "/" + data_type + "/*.json")

    total_SELECT_queries = 0
    total_DESCRIBE_queries = 0
    total_CONSTRUCT_queries = 0
    total_ASK_queries = 0

    scenario_one_queries = 0
    scenario_two_queries = 0
    scenario_three_queries = 0
    scenario_four_queries = 0

    scenario_five_queries = 0
    scenario_six_queries = 0
    scenario_seven_queries = 0
    scenario_eight_queries = 0

    scenario_nine_queries = 0
    scenario_ten_queries = 0
    scenario_eleven_queries = 0
    scenario_twelve_queries = 0

    scenario_filter_queries = 0
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

                        #print("New Query")
                        if scenario_one_detection.is_scenario_one(json_object, looking_for):
                            scenario_one_queries += 1
                        if scenario_two_detection.is_scenario_two(json_object, looking_for):
                            scenario_two_queries += 1
                        if scenario_three_detection.is_scenario_three(json_object, looking_for):
                            scenario_three_queries += 1
                        if scenario_four_detection.is_scenario_four(json_object, looking_for):
                            scenario_four_queries += 1

                        if scenario_five_detection.is_scenario_five(json_object, looking_for):
                            scenario_five_queries += 1
                        if scenario_six_detection.is_scenario_six(json_object, looking_for):
                            scenario_six_queries += 1
                        if scenario_seven_detection.is_scenario_seven(json_object, looking_for):
                            scenario_seven_queries += 1
                        if scenario_eight_detection.is_scenario_eight(json_object, looking_for):
                            scenario_eight_queries += 1

                        if scenario_nine_detection.is_scenario_nine(json_object, looking_for):
                            scenario_nine_queries += 1
                        if scenario_ten_detection.is_scenario_ten(json_object, looking_for):
                            scenario_ten_queries += 1
                        if scenario_eleven_detection.is_scenario_eleven(json_object, looking_for):
                            scenario_ten_queries += 1
                        if scenario_twelve_detection.is_scenario_twelve(json_object, looking_for):
                            scenario_ten_queries += 1

                        if scenario_filter_detection.is_scenario_filter(json_object, looking_for):
                            scenario_filter_queries += 1

                        #print(query_file)

                    elif json_object["queryType"] == "DESCRIBE":
                        total_DESCRIBE_queries += 1
                    elif json_object["queryType"] == "ASK":
                        total_ASK_queries += 1
                    elif json_object["queryType"] == "CONSTRUCT":
                        total_CONSTRUCT_queries += 1

        print("numbers ")
        print("scenario one: ", scenario_one_queries)
        print("scenario two: ", scenario_two_queries)
        print("scenario three: ", scenario_three_queries)
        print("scenario four: ", scenario_four_queries)

        print("scenario five: ", scenario_five_queries)
        print("scenario six: ", scenario_six_queries)
        print("scenario seven: ", scenario_seven_queries)
        print("scenario eight: ", scenario_eight_queries)

        print("scenario nine: ", scenario_nine_queries) # not yet tested
        print("scenario ten: ", scenario_ten_queries) # not yet tested
        print("scenario ekeven: ", scenario_eleven_queries) # not yet tested
        print("scenario twelve: ", scenario_twelve_queries) # not yet tested

        # not yet tested
        # print("scenario filter: ", scenario_filter_queries)

    return


def get_mode(data_type):
    if data_type == "reference_metadata/only_derived":
        return ["http://www.w3.org/ns/prov#wasDerivedFrom"]
    elif data_type == "reference_metadata/only_reference_property":
        return ["http://www.wikidata.org/prop/reference"]
    elif data_type == "reference_metadata/derived_+_reference_property":
        return ["http://www.wikidata.org/prop/reference", "http://www.w3.org/ns/prov#wasDerivedFrom"]
    elif data_type == "reference_metadata/only_reference_node":
        return ["http://www.wikidata.org/reference"]

