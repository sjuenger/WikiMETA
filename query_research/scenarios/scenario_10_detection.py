# method to detect scenario ten
#
#
#
# constellation for "wdref:1234567.."
# ( a reference node)
#
# scenario 10:
# wdref:.... ?p BOUND .
#
#
#
# look_for e.g. "http://www.wikidata.org/reference/0b1317d88f3e23f552ee804b79987760961819a0"


def scenario_ten_occurrences(json_object, look_for):
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

    # find scenarios 10

    result = 0

    # multiple bgp (basic graph patterns)
    for where_part in where:

        if where_part["type"] == "bgp":
            for triple in where_part["triples"]:

                if (triple["object"]["termType"] == "NamedNode") or ((triple["object"]["value"])
                                                                     in bound_variables.__str__()):

                    if ("termType" in triple["predicate"]):
                        # on property paths, there also could be no termType
                        if (triple["predicate"]["termType"] == "Variable") and ((triple["predicate"]["value"])
                                                                                not in bound_variables.__str__()):

                            if (triple["subject"]["termType"] == "NamedNode" and
                                    look_for in triple["subject"]["value"])\
                                    or (look_for == triple["subject"]["value"] and look_for in str(bound_variables)):
                                result += 1

    # if result:
    # print(result)
    # print("Scenario 1")
    # print(where)

    return result
