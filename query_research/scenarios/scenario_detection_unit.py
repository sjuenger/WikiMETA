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
import query_research.scenarios.scenario_six_detection as scenario_six_detection

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
                        if scenario_six_detection.is_scenario_one(json_object, looking_for):
                            if not scenario_one_detection.is_scenario_one(json_object, looking_for):
                                print("HERE")
                                print(query_file)

                        #print(query_file)

                    elif json_object["queryType"] == "DESCRIBE":
                        total_DESCRIBE_queries += 1
                    elif json_object["queryType"] == "ASK":
                        total_ASK_queries += 1
                    elif json_object["queryType"] == "CONSTRUCT":
                        total_CONSTRUCT_queries += 1

    print("scenario one: ", scenario_one_queries)
    print("scenario two: ", scenario_two_queries)
    print("scenario three: ", scenario_three_queries)
    print("scenario four: ", scenario_four_queries)

    return



def get_mode(data_type):
    if data_type == "reference_metadata/only_derived":
        return ["http://www.w3.org/ns/prov#wasDerivedFrom"]
    elif data_type == "reference_metadata/only_reference_node":
        return ["http://www.wikidata.org/prop/reference"]
    elif data_type == "reference_metadata/derived_+_reference_property":
        return ["http://www.wikidata.org/prop/reference", "http://www.w3.org/ns/prov#wasDerivedFrom"]

