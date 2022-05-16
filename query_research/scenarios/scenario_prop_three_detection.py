# method to detect scenario prop_three
#
#
#
# constellation for "wasDerivedFrom"
#
# scenario prop_three:
# BOUND prov:wasDerivedFrom ?o .
#
#
#
# look_for e.g. "http://www.w3.org/ns/prov#wasDerivedFrom"


def scenario_prop_three_occurrences(json_object, look_for, bound_variables):
    where = json_object["where"]

    # find scenarios prop_three

    result = 0

    # multiple bgp (basic graph patterns)
    for where_part in where:

        if "type" in where_part and where_part["type"] == "bgp":
            for triple in where_part["triples"]:

                if (triple["subject"]["termType"] == "NamedNode") or ((triple["subject"]["value"])
                                                                      in bound_variables.__str__()
                                                                        and triple["subject"]["termType"]
                                                                            == "Variable"):
                    # on property paths, there also could be no termType
                    if ("termType" in triple["predicate"]):
                        if ((triple["predicate"]["termType"] == "NamedNode" and
                             look_for in triple["predicate"]["value"]))\
                                or (look_for == triple["predicate"]["value"] and look_for in str(bound_variables)
                                    and triple["predicate"]["termType"] == "Variable"):

                            if (triple["object"]["termType"] == "Variable") and ((triple["object"]
                            ["value"]) not in bound_variables.__str__()):
                                result += 1

    return result
