# method to detect scenario eight
#
#
#
# constellation for "wdref:1234567.."
# ( a reference node)
#
# scenario 8:
# BOUND BOUND wdref:.... .
#
#
#
# look_for e.g. "<http://www.wikidata.org/reference/0b1317d88f3e23f552ee804b79987760961819a0>"


def is_scenario_eight(json_object, look_for):
    where = json_object["where"]

    # find BIND Variables
    bound_variables = []
    for where_part in where:
        if where_part["type"] == "bind":
            # print(where_part)
            # print(json_data.name)

            if "termType" in where_part["expression"]:
                if where_part["expression"]["termType"] == "namedNode":
                    if where_part["variable"]["termType"] == "Variable":
                        bound_variables.append(
                            (where_part["variable"]["value"], where_part["expression"]["value"]))
                print("Bound Variables: ")
                print(bound_variables)

    # find scenario 8

    result = False

    # multiple bgp (basic graph patterns)
    for where_part in where:

        if where_part["type"] == "bgp":
            for triple in where_part["triples"]:

                if (triple["subject"]["termType"] == "NamedNode") or ((triple["subject"]["value"])
                                                                      in bound_variables):

                    if ("termType" in triple["predicate"]):
                        # on property paths, there also could be no termType
                        if (triple["predicate"]["termType"] == "NamedNode") or ((triple["predicate"]["value"])
                                                                                in bound_variables):

                            if ((triple["object"]["termType"] == "NamedNode" and
                                 triple["object"]["value"].__contains__(look_for) )
                                    or (triple["object"]["termType"] == "Variable" and
                                        (triple["object"]["value"], look_for) in bound_variables)):
                                result = True

    # if result:
    # print(result)
    # print("Scenario 1")
    # print(where)

    return result
