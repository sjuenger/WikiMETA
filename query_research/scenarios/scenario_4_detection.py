# method to detect scenario four
#
#
#
# constellation for "wasDerivedFrom"
#
# scenario 4:
# BOUND prov:wasDerivedFrom BOUND .
#
#
#
# look_for e.g. "http://www.w3.org/ns/prov#wasDerivedFrom"


def scenario_four_occurrences(json_object, look_for, bound_variables):
    where = json_object["where"]

    # find scenarios 4

    result = 0

    # multiple bgp (basic graph patterns)
    for where_part in where:

        if where_part["type"] == "bgp":
            for triple in where_part["triples"]:

                if (triple["subject"]["termType"] == "NamedNode") or ((triple["subject"]["value"])
                                                                     in bound_variables.__str__()):
                    # on property paths, there also could be no termType
                    if ("termType" in triple["predicate"]):
                        if (triple["predicate"]["termType"] == "NamedNode" and
                              look_for in triple["predicate"]["value"])\
                                or (look_for == triple["predicate"]["value"] and look_for in str(bound_variables)):

                            if (triple["object"]["termType"] == "NamedNode") or ((triple["object"]
                            ["value"]) in bound_variables.__str__()):

                              result += 1

    return result
