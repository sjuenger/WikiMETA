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

# scenario 5:
# BIND( ...

# scenario X for DESCRIBE, CONSTRUCT, ...?



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
                        where = json_object["where"]

                        # find BIND Variables
                        bound_variables = []
                        for where_part in where:
                            if where_part["type"] == "bind":
                                #print(where_part)
                                #print(json_data.name)

                                if where_part["expression"]["type"] == "literal":
                                    if where_part["variable"]["termType"] == "Variable":
                                        bound_variables.append(
                                            (where_part["variable"]["value"], where_part["expression"]["value"]))
                                print(bound_variables)

                        # find scenario 1

                        # multiple bgp (basic graph patterns
                        for where_part in where:

                            if where_part["type"] == "bgp":

                                for triple in where_part["triples"]:

                                    if (triple["subject"]["termType"] == "Variable") or ((triple["subject"]["value"])
                                                                                         not in bound_variables):

                                        # predicate might also be a path
                                        if triple["predicate"]["termType"] is not None:

                                            if (((triple["predicate"]["termType"] == "NamedNode" and
                                                triple["predicate"]["value"] ==
                                                    "<http://www.w3.org/ns/prov#wasDerivedFrom>"))
                                                or ((triple["predicate"]["termType"] == "Variable" and
                                                     ((triple["predicate"]["value"],
                                                       "<http://www.w3.org/ns/prov#wasDerivedFrom>")
                                                    in bound_variables)))):

                                                if (triple["object"]["termType"] == "Variable") or ((triple["object"]
                                                ["value"]) not in bound_variables):

                                                    print("Stack Canary")

                                # find scenario 5

                                # multiple bgp
                            for where_part in where:

                                    if where_part["type"] == "bind":
                                        where_str = str(where_part)
                                        if "<http://www.w3.org/ns/prov#wasDerivedFrom>" in where_str:
                                            print(where_str)

                    elif json_object["queryType"] == "DESCRIBE":
                        total_DESCRIBE_queries += 1
                    elif json_object["queryType"] == "ASK":
                        total_ASK_queries += 1
                    elif json_object["queryType"] == "CONSTRUCT":
                        total_CONSTRUCT_queries += 1



                                #print("here")

    return



def get_mode(data_type):
    if data_type == "reference_metadata/only_derived":
        return ["<http://www.w3.org/ns/prov#wasDerivedFrom>"]
    elif data_type == "reference_metadata/only_reference_node":
        return ["<http://www.wikidata.org/prop/reference"]
    elif data_type == "reference_metadata/derived_+_reference_property":
        return ["<http://www.wikidata.org/prop/reference", "<http://www.w3.org/ns/prov#wasDerivedFrom>"]

