# method to detect scenario sub_two
#
#
#
# constellation for "wdref:1234567.."
# ( a reference node)
#
# scenario sub_two:
# wdref:.... ?p BOUND .
#
#
#
# look_for e.g. "http://www.wikidata.org/reference/0b1317d88f3e23f552ee804b79987760961819a0"


def scenario_sub_two_occurrences(json_object, look_for, bound_variables):
    where = json_object["where"]

    # find scenarios sub_two

    result = 0

    # multiple bgp (basic graph patterns)
    for where_part in where:

        if "type" in where_part and where_part["type"] == "bgp":
            for triple in where_part["triples"]:

                if (triple["object"]["termType"] == "NamedNode") or ((triple["object"]["value"])
                                                                     in bound_variables.__str__()
                                                                        and triple["object"]["termType"]
                                                                            == "Variable"):

                    if ("termType" in triple["predicate"]):
                        # on property paths, there also could be no termType
                        if (triple["predicate"]["termType"] == "Variable") and ((triple["predicate"]["value"])
                                                                                not in bound_variables.__str__()):

                            if (triple["subject"]["termType"] == "NamedNode" and
                                    look_for in triple["subject"]["value"])\
                                    or (look_for == triple["subject"]["value"] and look_for in str(bound_variables)
                                        and triple["subject"]["termType"] == "Variable"):
                                result += 1

    return result
