# method to detect scenario obj_two
#
#
#
# constellation for "wdref:1234567.."
# ( a reference node)
#
# scenario obj_two:
# ?s BOUND wdref:.... .
#
#
#
# look_for e.g. "http://www.wikidata.org/reference/0b1317d88f3e23f552ee804b79987760961819a0"


def scenario_obj_two_occurrences(json_object, look_for, bound_variables):
    where = json_object["where"]

    # find scenario obj_two

    result = 0

    # multiple bgp (basic graph patterns)
    for where_part in where:

        if "type" in where_part and where_part["type"] == "bgp":
            for triple in where_part["triples"]:

                if (triple["subject"]["termType"] == "Variable") and ((triple["subject"]["value"])
                                                                      not in bound_variables.__str__()):

                    if ("termType" in triple["predicate"]):
                        # on property paths, there also could be no termType
                        if (triple["predicate"]["termType"] == "NamedNode") or ((triple["predicate"]["value"])
                                                                                in bound_variables.__str__()
                                                                                    and triple["predicate"]["termType"]
                                                                                        == "Variable"):

                            if (triple["object"]["termType"] == "NamedNode" and
                                look_for in triple["object"]["value"]) \
                                    or (look_for == triple["object"]["value"] and look_for in str(bound_variables)
                                        and triple["object"]["termType"] == "Variable"):
                                result += 1

    return result
