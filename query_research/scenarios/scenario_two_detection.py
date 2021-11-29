# method to detect scenario two
#
#
#
# constellation for "wasDerivedFrom"
#
# scenario 2:
# BOUND prov:wasDerivedFrom ?o .
#
#
#
# look_for e.g. "<http://www.w3.org/ns/prov#wasDerivedFrom>"


def is_scenario_two(json_object, look_for):
    where = json_object["where"]

    # find BIND Variables
    bound_variables = []
    for where_part in where:
        if where_part["type"] == "bind":
            #print(where_part)
            #print(json_data.name)

            if "termType" in where_part["expression"]:
                if where_part["expression"]["termType"] == "namedNode":
                    if where_part["variable"]["termType"] == "Variable":
                        bound_variables.append(
                            (where_part["variable"]["value"], where_part["expression"]["value"]))
                print("Bound Variables: ")
                print(bound_variables)

    # find scenario 1

    result = False

    # multiple bgp (basic graph patterns)
    for where_part in where:

        if where_part["type"] == "bgp":
            for triple in where_part["triples"]:

                if (triple["subject"]["termType"] == "NamedNode") or ((triple["subject"]["value"])
                                                                     in bound_variables):
                    # on property paths, there also could be no termType
                    if ("termType" in triple["predicate"]):
                        if (((triple["predicate"]["termType"] == "NamedNode" and
                              triple["predicate"]["value"] == look_for))
                                or ((triple["predicate"]["termType"] == "Variable" and
                                     ((triple["predicate"]["value"],
                                       look_for)
                                      in bound_variables)))):

                            if (triple["object"]["termType"] == "Variable") and ((triple["object"]
                            ["value"]) not in bound_variables):

                              result = True
    #if result:
        #print(result)
        #print("Scenario 1")
        #print(where)

    return result
