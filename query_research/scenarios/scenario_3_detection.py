# method to detect scenario three
#
#
#
# constellation for "wasDerivedFrom"
#
# scenario 3:
# ?s prov:wasDerivedFrom BOUND .
#
#
#
# look_for e.g. "http://www.w3.org/ns/prov#wasDerivedFrom"


def scenario_three_occurrences(json_object, look_for):
    where = json_object["where"]

    # find BIND Variables
    bound_variables = []
    for where_part in where:
        if where_part["type"] == "bind":

            if "termType" in where_part["expression"]:
                if where_part["expression"]["termType"] == "NamedNode":
                    if where_part["variable"]["termType"] == "Variable":
                        bound_variables.append(
                            (where_part["variable"]["value"], where_part["expression"]["value"]))

    # find scenario 3

    result = 0

    # multiple bgp (basic graph patterns)
    for where_part in where:

        if where_part["type"] == "bgp":
            for triple in where_part["triples"]:

                if (triple["subject"]["termType"] == "Variable") and ((triple["subject"]["value"])
                                                                      not in bound_variables.__str__()):
                    # on property paths, there also could be no termType
                    if ("termType" in triple["predicate"]):
                        if (triple["predicate"]["termType"] == "NamedNode" and
                              look_for in triple["predicate"]["value"])\
                                or (look_for == triple["predicate"]["value"] and look_for in str(bound_variables)):
                            # TODO: BETTER METHOD, THAN JUST THIS STR -> use regex with x numbers behind the "P" also for other scenarios):

                            if (triple["object"]["termType"] == "NamedNode") or \
                                    ((triple["object"]["value"]) in bound_variables.__str__()):

                                result +=1
    # if result:
    # print(result)
    # print("Scenario 1")
    # print(where)

    return result
