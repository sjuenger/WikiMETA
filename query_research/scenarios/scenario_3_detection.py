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


def scenario_three_occurrences(json_object, look_for, bound_variables):
    where = json_object["where"]

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
                                or (look_for == triple["predicate"]["value"] and look_for in str(bound_variables)
                                    and triple["predicate"]["termType"] == "Variable"):
                            # TODO: BETTER METHOD, THAN JUST THIS STR -> use regex with x numbers behind the "P" also for other scenarios):

                            if (triple["object"]["termType"] == "NamedNode") or \
                                    ((triple["object"]["value"]) in bound_variables.__str__()
                                        and triple["object"]["termType"] == "Variable"):

                                result += 1

    return result
